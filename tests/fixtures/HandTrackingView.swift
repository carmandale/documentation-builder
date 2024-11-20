import SwiftUI
import RealityKit
import ARKit

struct HandTrackingView: View {
    @State private var handPosition: SIMD3<Float>?
    @State private var isGrabbing = false
    
    var body: some View {
        RealityView { content in
            // Setup hand tracking
            let handTrackingSystem = content.handTrackingSystem
            handTrackingSystem?.isEnabled = true
            
            // Create interactive entity
            let sphere = ModelEntity(mesh: .generateSphere(radius: 0.05))
            sphere.components[HandTrackingComponent.self] = HandTrackingComponent()
            
            content.add(sphere)
        }
        .handTracking(.continuous) { hand in
            // Update hand position
            handPosition = hand.position
            
            // Detect grab gesture
            isGrabbing = hand.isGrabbing
        }
        .privacyInfo("Hand tracking is used for gesture interaction")
    }
}
