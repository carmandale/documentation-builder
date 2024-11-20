import SwiftUI
import RealityKit
import RealityKitContent

struct ImmersiveSpaceView: View {
    @Environment(\.openImmersiveSpace) var openImmersiveSpace
    @Environment(\.dismissImmersiveSpace) var dismissImmersiveSpace
    
    var body: some View {
        VStack {
            RealityView { content in
                // Load 3D model
                if let entity = try? await Entity(named: "Scene", in: realityKitContentBundle) {
                    content.add(entity)
                    
                    // Add anchoring
                    if let anchorEntity = entity.findEntity(named: "Anchor") as? AnchorEntity {
                        anchorEntity.position = SIMD3(x: 0, y: 1.5, z: -2)
                    }
                }
            }
            .gesture(TapGesture().targetedToAnyEntity().onEnded { _ in
                // Handle taps on 3D content
            })
        }
        .task {
            // Request immersive space
            await openImmersiveSpace(id: "ImmersiveSpace")
        }
    }
}
