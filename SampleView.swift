import SwiftUI
import RealityKit
import Combine

struct SampleView: View {
    // Timer publisher for continuous animation
    @State private var cancellable: AnyCancellable?
    
    var body: some View {
        HStack {
            // 2D Window Content
            VStack {
                Text("VisionOS Sample View")
                    .font(.title)
                    .padding()
                
                Image(systemName: "vision.pro")
                    .resizable()
                    .scaledToFit()
                    .frame(width: 100, height: 100)
                    .padding()
            }
            .padding()
            .frame(width: 400)
            
            // 3D Content
            RealityView { content in
                // Create cylinder
                let cylinder = ModelEntity(
                    mesh: .generateCylinder(height: 0.2, radius: 0.1),
                    materials: [SimpleMaterial(color: .blue, isMetallic: true)]
                )
                
                // Set initial transform - first rotate 45° on Z
                cylinder.transform = Transform(
                    rotation: simd_quatf(
                        angle: .pi / 4,
                        axis: SIMD3<Float>(0, 0, 1)
                    )
                )
                
                // Add cylinder to content
                content.add(cylinder)
                
                // Setup continuous rotation animation
                let rotationAnimation = cylinder.scene?.subscribe(to: TimelineSchedule(repeating: .seconds(1/30))) { _ in
                    cylinder.transform.rotation = simd_quatf(
                        angle: cylinder.transform.rotation.angle + 0.02,
                        axis: SIMD3<Float>(0, 1, 0)
                    ).concatenated(with: cylinder.transform.rotation)
                }
                
                if let rotationAnimation = rotationAnimation {
                    cancellable = AnyCancellable(rotationAnimation)
                }
            }
            .frame(width: 400, height: 400)
        }
    }
}

#Preview {
    SampleView()
} 