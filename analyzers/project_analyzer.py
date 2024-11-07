from pathlib import Path
from typing import List, Dict, Optional
import logging
import re

logger = logging.getLogger(__name__)

class ProjectAnalyzer:
    """Analyzes downloaded Xcode projects for patterns and examples"""
    
    def __init__(self, projects_dir: Path = Path('data/projects')):
        self.projects_dir = projects_dir
    
    def analyze_project(self, project_path: Path) -> Dict[str, any]:
        """Analyze a downloaded project"""
        try:
            # Find Swift files
            swift_files = list(project_path.rglob('*.swift'))
            logger.info(f"Found {len(swift_files)} Swift files")
            
            patterns = {
                '3d_content': {'count': 0, 'files': []},
                'animation': {'count': 0, 'files': []},
                'ui_components': {'count': 0, 'files': []},
                'gestures': {'count': 0, 'files': []},
                'spatial_audio': {'count': 0, 'files': []},
                'immersive_spaces': {'count': 0, 'files': []}
            }
            
            for file in swift_files:
                content = file.read_text()
                logger.info(f"\nAnalyzing {file.name}:")
                
                # Look for specific patterns
                if 'RealityKit' in content:
                    patterns['3d_content']['count'] += 1
                    patterns['3d_content']['files'].append(file.name)
                if 'animation' in content.lower() or 'animate' in content.lower():
                    patterns['animation']['count'] += 1
                    patterns['animation']['files'].append(file.name)
                if 'View' in content or 'Button' in content:
                    patterns['ui_components']['count'] += 1
                    patterns['ui_components']['files'].append(file.name)
                if 'gesture' in content.lower() or 'tap' in content.lower():
                    patterns['gestures']['count'] += 1
                    patterns['gestures']['files'].append(file.name)
                if 'AudioEngine' in content or 'spatialAudio' in content:
                    patterns['spatial_audio']['count'] += 1
                    patterns['spatial_audio']['files'].append(file.name)
                if 'ImmersiveSpace' in content:
                    patterns['immersive_spaces']['count'] += 1
                    patterns['immersive_spaces']['files'].append(file.name)
            
            return {
                'patterns': patterns,
                'usage': {},  # Deprecated
                'validation': {}  # Deprecated
            }
            
        except Exception as e:
            logger.error(f"Error analyzing project: {str(e)}")
            return {}
    
    def _extract_code_block(self, content: str, pattern: str, context_lines: int = 5) -> str:
        """Extract code block around a pattern with context"""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if pattern in line:
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                return '\n'.join(lines[start:end])
        return ""
    
    def analyze_api_patterns(self, content: str) -> Dict[str, any]:
        """Analyze how APIs are used in the code"""
        api_patterns = {
            'container_types': {},  # Track what container types are used
            'method_usage': {},     # Track how methods are called
            'common_patterns': []   # Track recurring patterns
        }
        
        # Example: Track EventSubscription usage
        if 'EventSubscription' in content:
            container_match = re.search(
                r'(var|let)\s+\w+\s*:\s*(\[|\{).*EventSubscription', 
                content
            )
            if container_match:
                container_type = 'Array' if container_match.group(2) == '[' else 'Set'
                api_patterns['container_types']['EventSubscription'] = container_type
                
        # Track quaternion operations
        if 'simd_quatf' in content:
            for line in content.split('\n'):
                if 'simd_quatf' in line:
                    if '*' in line:
                        api_patterns['method_usage'].setdefault('quaternion', set()).add('multiplication')
                    if 'concatenated' in line:
                        api_patterns['method_usage'].setdefault('quaternion', set()).add('concatenation')
        
        return api_patterns
    
    def _analyze_animation_pattern(self, content: str, filename: str, patterns: Dict, usage: Dict):
        """Analyze animation state machine patterns"""
        animation_matches = [
            line.strip()
            for line in content.split('\n')
            if 'AnimationState' in line and not line.strip().startswith('//')
        ]
        if animation_matches:
            pattern_key = 'animation_state_machine'
            usage[pattern_key] = usage.get(pattern_key, 0) + 1
            patterns['animation'].append({
                'file': filename,
                'type': 'state_machine',
                'content': '\n'.join(animation_matches),
                'context': self._extract_code_block(content, animation_matches[0], 15)
            })
    
    def _analyze_patterns(self, content: str, filename: str, patterns: Dict, usage: Dict, validation: Dict):
        """Analyze code for specific patterns"""
        try:
            if 'RealityKit' in content:
                # Look for attachments first since they're most specific
                if any(x in content for x in ['RealityView { content, attachments', 'Attachment(id:']):
                    self._analyze_attachment_pattern(content, filename, patterns, usage)
                
                # Rest of patterns...
                self._analyze_animation_pattern(content, filename, patterns, usage)
                self._analyze_transform_pattern(content, filename, patterns, usage)
                self._analyze_subscription_pattern(content, filename, patterns, usage)
                    
        except Exception as e:
            logger.error(f"Error analyzing patterns in {filename}: {str(e)}")
    
    def _analyze_transform_pattern(self, content: str, filename: str, patterns: Dict, usage: Dict):
        """Analyze transform and rotation patterns"""
        transform_matches = [
            line.strip()
            for line in content.split('\n')
            if 'transform' in line and ('rotation' in line or 'simd_quatf' in line)
            and not line.strip().startswith('//')
        ]
        if transform_matches:
            pattern_key = 'transform_rotation'
            usage[pattern_key] = usage.get(pattern_key, 0) + 1
            patterns['transforms'].append({
                'file': filename,
                'type': 'rotation',
                'content': '\n'.join(transform_matches),
                'context': self._extract_code_block(content, transform_matches[0], 15)
            })
    
    def _analyze_subscription_pattern(self, content: str, filename: str, patterns: Dict, usage: Dict):
        """Analyze event subscription patterns"""
        subscription_matches = [
            line.strip()
            for line in content.split('\n')
            if 'subscribe' in line and not line.strip().startswith('//')
        ]
        if subscription_matches:
            pattern_key = 'event_subscription'
            usage[pattern_key] = usage.get(pattern_key, 0) + 1
            patterns['ui_components'].append({
                'file': filename,
                'type': 'subscription',
                'content': '\n'.join(subscription_matches),
                'context': self._extract_code_block(content, subscription_matches[0], 15)
            })
    
    def _analyze_video_pattern(self, content: str, filename: str, patterns: Dict, usage: Dict):
        """Analyze video playback patterns"""
        video_matches = [
            line.strip()
            for line in content.split('\n')
            if any(x in line for x in ['VideoPlayer', 'AVPlayer', 'play()', '.rate'])
            and not line.strip().startswith('//')
        ]
        if video_matches:
            pattern_key = 'video_playback'
            usage[pattern_key] = usage.get(pattern_key, 0) + 1
            patterns['media'].append({
                'file': filename,
                'type': 'video',
                'content': '\n'.join(video_matches),
                'context': self._extract_code_block(content, video_matches[0], 15)
            })
    
    def _analyze_audio_pattern(self, content: str, filename: str, patterns: Dict, usage: Dict):
        """Analyze spatial audio patterns"""
        audio_matches = [
            line.strip()
            for line in content.split('\n')
            if any(x in line for x in ['AudioEngine', 'spatialAudio', 'playSound'])
            and not line.strip().startswith('//')
        ]
        if audio_matches:
            pattern_key = 'spatial_audio'
            usage[pattern_key] = usage.get(pattern_key, 0) + 1
            patterns['media'].append({
                'file': filename,
                'type': 'audio',
                'content': '\n'.join(audio_matches),
                'context': self._extract_code_block(content, audio_matches[0], 15)
            })
    
    def _analyze_surface_detection_pattern(self, content: str, filename: str, patterns: Dict, usage: Dict):
        """Analyze surface detection patterns"""
        surface_matches = [
            line.strip()
            for line in content.split('\n')
            if any(x in line for x in [
                'CollisionEvents',
                'AnchorEntity',
                'planeAlignment',
                'horizontalAlignment',
                'verticalAlignment',
                'attachments',
                'placementGestures',
                'collisionEnabled',
                'dragRotationEnabled',
                'gravityAligned',
                'PlaneAnchor',
                'PlacementManager',
                'PlacementState'
            ])
            and not line.strip().startswith('//')
        ]
        if surface_matches:
            pattern_key = 'surface_detection'
            usage[pattern_key] = usage.get(pattern_key, 0) + 1
            patterns['3d_content'].append({
                'file': filename,
                'type': 'surface_detection',
                'content': '\n'.join(surface_matches),
                'context': self._extract_code_block(content, surface_matches[0], 15)
            })
    
    def _analyze_window_pattern(self, content: str, filename: str, patterns: Dict, usage: Dict):
        """Analyze window management patterns"""
        window_matches = [
            line.strip()
            for line in content.split('\n')
            if any(x in line for x in ['WindowGroup', 'openWindow', 'dismissWindow'])
            and not line.strip().startswith('//')
        ]
        if window_matches:
            pattern_key = 'window_management'
            usage[pattern_key] = usage.get(pattern_key, 0) + 1
            patterns['ui_components'].append({
                'file': filename,
                'type': 'window',
                'content': '\n'.join(window_matches),
                'context': self._extract_code_block(content, window_matches[0], 15)
            })
    
    def _analyze_spatial_photo_pattern(self, content: str, filename: str, patterns: Dict, usage: Dict):
        """Analyze spatial photo patterns"""
        photo_matches = [
            line.strip()
            for line in content.split('\n')
            if any(x in line for x in ['SpatialPhoto', 'PhotosPicker', 'PhotosUI'])
            and not line.strip().startswith('//')
        ]
        if photo_matches:
            pattern_key = 'spatial_photo'
            usage[pattern_key] = usage.get(pattern_key, 0) + 1
            patterns['media'].append({
                'file': filename,
                'type': 'spatial_photo',
                'content': '\n'.join(photo_matches),
                'context': self._extract_code_block(content, photo_matches[0], 15)
            })
    
    def _analyze_attachment_pattern(self, content: str, filename: str, patterns: Dict, usage: Dict):
        """Analyze patterns for SwiftUI view attachments in RealityKit scenes"""
        attachment_matches = [
            line.strip()
            for line in content.split('\n')
            if any(x in line for x in [
                'RealityView { content, attachments in',  # RealityView with attachments
                'update: { content, attachments in',      # Update closure with attachments
                'attachments.entity(for:',                # Getting attachment entity
                'Attachment(id:',                         # Creating attachment
                'addChild(',                             # Adding attachment to entity
                '.position =',                           # Positioning attachment
                '.scale =',                              # Scaling attachment
                'attachments:',                          # Attachments closure
                'makeContentView',                       # Creating SwiftUI view
                'viewTarget',                            # Setting view target
                'contentEntity',                         # Content entity
                'attachedTo',                            # Attachment relationship
                'attachmentBounds',                      # Setting attachment bounds
                'attachmentPolicy',                      # Attachment policy
                'ViewAttachmentEntity',                  # View attachment entity
                'view.attach(',                          # Direct view attachment
                'view.detach(',                          # Detaching views
                'view.attachments'                       # Managing attachments
            ])
            and not line.strip().startswith('//')
        ]
        if attachment_matches:
            pattern_key = 'view_attachment'
            usage[pattern_key] = usage.get(pattern_key, 0) + 1
            patterns['ui_components'].append({
                'file': filename,
                'type': 'view_attachment',
                'content': '\n'.join(attachment_matches),
                'context': self._extract_code_block(content, attachment_matches[0], 15)
            })