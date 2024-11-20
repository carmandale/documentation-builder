from typing import Dict, List, Optional
from pathlib import Path
import json
from .development_plan import DevelopmentPlan, AppType, FeatureRequirement, DevelopmentStage
from patterns.visionos_patterns import VisionOSPattern, get_pattern

class DevelopmentPlanLoader:
    """Loads and manages development plan templates."""
    
    def __init__(self, data_dir: Path = Path('data/development_plans')):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.plans: Dict[str, DevelopmentPlan] = {}
        self._load_plans()
    
    def get_plan(self, app_type: AppType, features: List[FeatureRequirement]) -> Optional[DevelopmentPlan]:
        """Get a development plan matching the requirements."""
        # Find best matching plan
        best_match = None
        best_score = 0
        
        for plan in self.plans.values():
            score = self._calculate_match_score(plan, app_type, features)
            if score > best_score:
                best_score = score
                best_match = plan
        
        return best_match
    
    def _calculate_match_score(self, plan: DevelopmentPlan, 
                             app_type: AppType,
                             features: List[FeatureRequirement]) -> int:
        """Calculate how well a plan matches the requirements."""
        score = 0
        
        # App type is most important
        if plan.app_type == app_type:
            score += 100
            
        # Feature matches
        for feature in features:
            if feature in plan.features:
                score += 10
                
        return score
    
    def save_plan(self, name: str, plan: DevelopmentPlan):
        """Save a development plan template."""
        self.plans[name] = plan
        
        # Save to disk
        plan_file = self.data_dir / f"{name}.json"
        plan_data = plan.dict()
        
        # Convert patterns to names for serialization
        for stage in plan_data['development_stages']:
            stage['patterns'] = [p.name for p in stage['patterns']]
        
        plan_file.write_text(json.dumps(plan_data, indent=2))
    
    def _load_plans(self):
        """Load all development plan templates."""
        for plan_file in self.data_dir.glob("*.json"):
            try:
                plan_data = json.loads(plan_file.read_text())
                
                # Convert pattern names back to patterns
                for stage in plan_data['development_stages']:
                    stage['patterns'] = [
                        get_pattern(name) for name in stage['patterns']
                    ]
                
                plan = DevelopmentPlan(**plan_data)
                self.plans[plan_file.stem] = plan
            except Exception as e:
                print(f"Error loading plan {plan_file}: {e}")
    
    def get_plan_suggestions(self, description: str) -> List[DevelopmentPlan]:
        """Get development plan suggestions based on description."""
        suggestions = []
        keywords = description.lower().split()
        
        for plan in self.plans.values():
            # Check if plan matches description keywords
            plan_text = (
                plan.description.lower() + " " +
                plan.architecture_overview.lower() + " " +
                " ".join(cap.lower() for cap in plan.required_capabilities)
            )
            
            matches = sum(1 for keyword in keywords if keyword in plan_text)
            if matches > len(keywords) / 2:  # More than 50% match
                suggestions.append(plan)
        
        return suggestions

    def create_custom_plan(self, base_plan: DevelopmentPlan, 
                          modifications: Dict) -> DevelopmentPlan:
        """Create a custom plan based on an existing template."""
        # Start with base plan
        plan_data = base_plan.dict()
        
        # Apply modifications
        for key, value in modifications.items():
            if key in plan_data:
                plan_data[key] = value
        
        return DevelopmentPlan(**plan_data)
