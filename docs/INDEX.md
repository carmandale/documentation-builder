# VisionOS Documentation Analyzer Documentation

## Getting Started
- [Quick Start Guide](guides/QUICKSTART.md) - Get up and running
- [Development Guide](guides/DEVELOPMENT.md) - Development setup and workflow
- [Contributing Guide](guides/CONTRIBUTING.md) - How to contribute

## Technical Documentation
- [Architecture](technical/ARCHITECTURE.md) - System architecture overview
- [Pattern System](technical/PATTERNS.md) - Pattern detection and refinement
- [Caching System](technical/CACHING.md) - Cache management
- [Relationships](technical/RELATIONSHIPS.md) - Relationship tracking

## API Reference
- [Analyzers](api/ANALYZERS.md) - Pattern and project analysis
- [Extractors](api/EXTRACTORS.md) - Content extraction
- [Core](api/CORE.md) - Core functionality
- [Models](api/MODELS.md) - Data models

## Practical Examples

### 1. 2D View with Rotating 3D Object
```swift
import SwiftUI
import RealityKit

struct RotatingObjectView: View {
    @State private var rotationAngle: Float = 0.0
    
    var body: some View {
        VStack {
            // Header with text and image
            HStack {
                Text("Rotating Model")
                    .font(.title)
                Image("icon")
                    .resizable()
                    .frame(width: 40, height: 40)
            }
            
            // 3D content in RealityView
            RealityView { content in
                // Create simple cube entity
                let mesh = MeshResource.generateBox(size: 0.2)
                let material = SimpleMaterial(color: .blue, roughness: 0.5)
                let entity = ModelEntity(mesh: mesh, materials: [material])
                
                // Add to scene
                content.add(entity)
                
                // Start rotation animation
                entity.components[RotationComponent.self] = RotationComponent()
            } update: { content in
                // Update rotation
                if let entity = content.entities.first {
                    entity.transform.rotation *= simd_quatf(
                        angle: .pi / 180,  // 1 degree per frame
                        axis: [0, 1, 0]    // Rotate around Y axis
                    )
                }
            }
            .frame(width: 300, height: 300)
            
            // Footer text
            Text("Tap to interact")
                .font(.caption)
        }
        .padding()
    }
}

// Custom rotation component
struct RotationComponent: Component {
    var speed: Float = 1.0
}
```

### 2. Immersive Space with Scene Understanding
```swift
import SwiftUI
import RealityKit
import ARKit

struct ImmersiveSpaceView: View {
    @StateObject private var sceneManager = SceneManager()
    
    var body: some View {
        RealityView { content in
            // Set up scene
            sceneManager.setupScene(content)
        } update: { content in
            // Update scene
            sceneManager.updateScene(content)
        }
    }
}

class SceneManager: ObservableObject {
    private let session = ARSession()
    
    func setupScene(_ content: RealityViewContent) {
        // Configure AR session
        let config = ARWorldTrackingConfiguration()
        config.sceneReconstruction = .mesh
        config.planeDetection = [.horizontal, .vertical]
        
        session.run(config)
        
        // Add ambient light
        let ambientLight = Entity()
        ambientLight.components[EnvironmentLightComponent.self] = .init()
        content.add(ambientLight)
    }
    
    func updateScene(_ content: RealityViewContent) {
        // Update scene based on AR anchors
        session.currentFrame?.anchors.forEach { anchor in
            switch anchor {
            case let planeAnchor as ARPlaneAnchor:
                handlePlaneAnchor(planeAnchor, in: content)
            case let meshAnchor as ARMeshAnchor:
                handleMeshAnchor(meshAnchor, in: content)
            default:
                break
            }
        }
    }
}
```

### More Examples
- [Pattern Examples](examples/PATTERNS.md)
- [Integration Examples](examples/INTEGRATION.md)
- [Best Practices](examples/BEST_PRACTICES.md) 