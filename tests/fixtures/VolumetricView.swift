import SwiftUI
import RealityKit

struct VolumetricView: View {
    @State private var showVolume = true
    
    var body: some View {
        RealityView { content in
            // Create volumetric material
            var material = VolumetricMaterial()
            material.scattering = .init(0.2)
            material.absorption = .init(0.1)
            
            // Create volumetric entity
            let mesh = MeshResource.generateBox(size: 0.2)
            let entity = ModelEntity(mesh: mesh, materials: [material])
            
            // Add to scene
            content.add(entity)
        }
        .volumetric(showVolume)
        .frame(depth: 0.3)
        .sensoryFeedback(.impact, trigger: showVolume)
    }
}
