.
├── analyzers
│   ├── __init__.py
│   ├── component_analyzer.py
│   ├── documentation_analyzer.py
│   ├── llm_interface.py
│   ├── pattern_evolution.py
│   ├── pattern_refiner.py
│   ├── project_analyzer.py
│   ├── relationship_tracker.py
│   └── topic_analyzer.py
├── cli
│   ├── __init__.py
│   └── scraper_cli.py
├── core
│   ├── __init__.py
│   ├── config.py
│   ├── documentation_analyzer.py
│   ├── feature_tracking.py
│   ├── knowledge_base.py
│   ├── llm_interface.py
│   ├── prompt_templates.py
│   ├── scraper.py
│   └── url_sources.py
├── data
│   ├── cache
│   │   ├── analysis_cache.json
│   │   ├── discovered_samples.json
│   │   ├── documentation_cache.json
│   │   └── url_cache.json
│   ├── debug
│   │   ├── _content.html
│   │   ├── _initial.html
│   │   ├── _structure.html
│   │   ├── bot-anist.html
│   │   ├── bot-anist_after_wait.html
│   │   ├── bot-anist_initial.html
│   │   ├── bot-anist_raw.html
│   │   ├── designing-for-visionos.html
│   │   ├── designing-for-visionos_content.html
│   │   ├── designing-for-visionos_initial.html
│   │   ├── designing-for-visionos_structure.html
│   │   ├── destination-video.html
│   │   ├── developer.apple.com_initial.html
│   │   ├── diorama.html
│   │   ├── found_samples.txt
│   │   ├── immersive-experiences.html
│   │   ├── immersive-experiences_content.html
│   │   ├── immersive-experiences_initial.html
│   │   ├── immersive-experiences_structure.html
│   │   ├── intro_samples_page.html
│   │   ├── introductory-visionos-samples_structure.html
│   │   ├── playing-spatial-audio-in-visionos.html
│   │   ├── playing-spatial-audio-in-visionos_after_wait.html
│   │   ├── playing-spatial-audio-in-visionos_initial.html
│   │   ├── playing-spatial-audio-in-visionos_raw.html
│   │   ├── raw_.html
│   │   ├── raw_adding-3d-content-to-your-app.html
│   │   ├── raw_bot-anist.html
│   │   ├── raw_creating-fully-immersive-experiences.html
│   │   ├── raw_creating-immersive-spaces-in-visionos-with-swiftui.html
│   │   ├── raw_creating-your-first-visionos-app.html
│   │   ├── raw_designing-for-visionos.html
│   │   ├── raw_immersive-experiences.html
│   │   ├── raw_swift-splash.html
│   │   ├── raw_visionos.html
│   │   ├── swift-splash.html
│   │   ├── visionos.html
│   │   ├── world.html
│   │   ├── world_after_wait.html
│   │   ├── world_initial.html
│   │   └── world_raw.html
│   ├── docs
│   │   └── debug_creating-3d-shapes-in-visionos-with-realitykit.html
│   ├── documentation
│   │   ├── adding-3d-content-to-your-app.json
│   │   ├── adding-a-depth-effect-to-text-in-visionos.json
│   │   └── incorporating-real-world-surroundings-in-an-immersive-experience.json
│   ├── extracted
│   │   ├── relationships
│   │   │   └── relationships.json
│   │   ├── extracted_adding-3d-content-to-your-app.json
│   │   ├── extracted_bot-anist.json
│   │   ├── extracted_creating-fully-immersive-experiences.json
│   │   ├── extracted_creating-immersive-spaces-in-visionos-with-swiftui.json
│   │   ├── extracted_creating-your-first-visionos-app.json
│   │   └── extracted_swift-splash.json
│   ├── knowledge
│   │   ├── patterns.json
│   │   ├── refined_patterns.json
│   │   └── relationships.json
│   ├── logs
│   │   └── scraper.log
│   ├── projects
│   │   ├── AddingADepthEffectToTextInVisionOS
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── DepthText
│   │   │   │   ├── App
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── EntryPoint.swift
│   │   │   │   │   └── Info.plist
│   │   │   │   └── Views
│   │   │   │       ├── DepthTextView.swift
│   │   │   │       └── MainView.swift
│   │   │   ├── DepthText.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── ApplyingMeshToRealWorldSurroundings
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── SceneReconstruction
│   │   │   │   ├── App
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── EntryPoint.swift
│   │   │   │   │   └── Info.plist
│   │   │   │   ├── Extensions
│   │   │   │   │   ├── ARKit.swift
│   │   │   │   │   ├── Entity.swift
│   │   │   │   │   └── MeshResource.swift
│   │   │   │   ├── Generators
│   │   │   │   │   └── MeshAnchorGenerator.swift
│   │   │   │   └── Views
│   │   │   │       ├── MainView.swift
│   │   │   │       └── SceneReconstructionView.swift
│   │   │   ├── SceneReconstruction.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── BOTAnist
│   │   │   ├── BOT-anist
│   │   │   │   ├── Assets.xcassets
│   │   │   │   │   ├── AccentColor.colorset
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── HeroRobot.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── HeroRobot@2x.png
│   │   │   │   │   ├── VisionOSAppIcon.solidimagestack
│   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   ├── Back.png
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   └── Front.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── backpack1.imageset
│   │   │   │   │   │   ├── BP1 (2) 1.png
│   │   │   │   │   │   ├── BP1 (2).png
│   │   │   │   │   │   ├── BP1_dark (2).png
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── backpack2.imageset
│   │   │   │   │   │   ├── BP2 (2) 1.png
│   │   │   │   │   │   ├── BP2 (2).png
│   │   │   │   │   │   ├── BP2_dark (2).png
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── backpack3.imageset
│   │   │   │   │   │   ├── BP3 (2) 1.png
│   │   │   │   │   │   ├── BP3 (2).png
│   │   │   │   │   │   ├── BP3_dark (2).png
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── body1.imageset
│   │   │   │   │   │   ├── B1 1.png
│   │   │   │   │   │   ├── B1.png
│   │   │   │   │   │   ├── B1_dark.png
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── body2.imageset
│   │   │   │   │   │   ├── B2 1.png
│   │   │   │   │   │   ├── B2.png
│   │   │   │   │   │   ├── B2_dark.png
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── body3.imageset
│   │   │   │   │   │   ├── B3 1.png
│   │   │   │   │   │   ├── B3.png
│   │   │   │   │   │   ├── B3_dark.png
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── circle.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   ├── oval 1.png
│   │   │   │   │   │   ├── oval.png
│   │   │   │   │   │   └── oval_dark.png
│   │   │   │   │   ├── head1.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   ├── H1 (1) 1.png
│   │   │   │   │   │   ├── H1 (1).png
│   │   │   │   │   │   └── H1_dark (1).png
│   │   │   │   │   ├── head2.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   ├── H2 (1) 1.png
│   │   │   │   │   │   ├── H2 (1).png
│   │   │   │   │   │   └── H2_dark (1).png
│   │   │   │   │   ├── head3.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   ├── H3 (1) 1.png
│   │   │   │   │   │   ├── H3 (1).png
│   │   │   │   │   │   └── H3_dark (1).png
│   │   │   │   │   ├── heart.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   ├── hearts 1.png
│   │   │   │   │   │   ├── hearts.png
│   │   │   │   │   │   └── hearts_dark.png
│   │   │   │   │   ├── iOSAppIcon.appiconset
│   │   │   │   │   │   ├── AppIcon.png
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   ├── DarkAppIcon.png
│   │   │   │   │   │   └── TintableAppIcon.png
│   │   │   │   │   ├── macOSAppIcon.appiconset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   ├── icon_128x128.png
│   │   │   │   │   │   ├── icon_128x128@2x.png
│   │   │   │   │   │   ├── icon_16x16.png
│   │   │   │   │   │   ├── icon_16x16@2x.png
│   │   │   │   │   │   ├── icon_256x256.png
│   │   │   │   │   │   ├── icon_256x256@2x.png
│   │   │   │   │   │   ├── icon_32x32.png
│   │   │   │   │   │   ├── icon_32x32@2x.png
│   │   │   │   │   │   ├── icon_512x512.png
│   │   │   │   │   │   └── icon_512x512@2x.png
│   │   │   │   │   ├── mesh.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── mesh.png
│   │   │   │   │   ├── metal.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── metal.png
│   │   │   │   │   ├── plastic.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── plastic.png
│   │   │   │   │   ├── rainbow.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── rainbow.png
│   │   │   │   │   ├── square.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   ├── digitalSquares (1) 1.png
│   │   │   │   │   │   ├── digitalSquares (1).png
│   │   │   │   │   │   └── digitalSquares.png
│   │   │   │   │   └── Contents.json
│   │   │   │   ├── Components
│   │   │   │   │   └── JointPinComponent.swift
│   │   │   │   ├── Extensions
│   │   │   │   │   ├── CaseIterableExtensions.swift
│   │   │   │   │   ├── ColorExtensions.swift
│   │   │   │   │   ├── EntityExtensions.swift
│   │   │   │   │   ├── Preview+AppStateEnvironment.swift
│   │   │   │   │   ├── RealityView+KeyboardControls.swift
│   │   │   │   │   ├── RealityView+TouchControls.swift
│   │   │   │   │   └── StringExtensions.swift
│   │   │   │   ├── Preview Content
│   │   │   │   │   └── Preview Assets.xcassets
│   │   │   │   │       └── Contents.json
│   │   │   │   ├── Robot
│   │   │   │   │   ├── AnimationStateMachine.swift
│   │   │   │   │   ├── RobotCharacter+Movement.swift
│   │   │   │   │   ├── RobotCharacter.swift
│   │   │   │   │   ├── RobotData.swift
│   │   │   │   │   ├── RobotProvider+Loading.swift
│   │   │   │   │   └── RobotProvider.swift
│   │   │   │   ├── Skybox
│   │   │   │   │   └── autumn_field_puresky_1k.png
│   │   │   │   ├── Systems
│   │   │   │   │   └── JointPinSystem.swift
│   │   │   │   ├── Views
│   │   │   │   │   ├── ContentView.swift
│   │   │   │   │   ├── ExplorationView.swift
│   │   │   │   │   ├── OrnamentView.swift
│   │   │   │   │   ├── RobotCustomizationView.swift
│   │   │   │   │   ├── RobotView.swift
│   │   │   │   │   ├── SelectorViews.swift
│   │   │   │   │   └── StartScreenView.swift
│   │   │   │   ├── AppState+Exploration.swift
│   │   │   │   ├── AppState.swift
│   │   │   │   ├── BOT-anist-InfoPlist.xcstrings
│   │   │   │   ├── BOT-anist.entitlements
│   │   │   │   ├── BOTanistApp.swift
│   │   │   │   ├── Localizable.xcstrings
│   │   │   │   └── PlantAnimationProvider.swift
│   │   │   ├── BOT-anist.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── BOTanist.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── Packages
│   │   │   │   └── BOTanistAssets
│   │   │   │       ├── Package.realitycomposerpro
│   │   │   │       │   ├── ProjectData
│   │   │   │       │   │   └── main.json
│   │   │   │       │   └── WorkspaceData
│   │   │   │       │       └── Settings.rcprojectdata
│   │   │   │       ├── Sources
│   │   │   │       │   └── BOTanistAssets
│   │   │   │       │       ├── BOTanistAssets.rkassets
│   │   │   │       │       │   ├── Assets
│   │   │   │       │       │   │   ├── Robot
│   │   │   │       │       │   │   │   ├── animations
│   │   │   │       │       │   │   │   │   ├── body1
│   │   │   │       │       │   │   │   │   │   ├── body1_celebrate_anim.usd
│   │   │   │       │       │   │   │   │   │   ├── body1_idle_anim.usd
│   │   │   │       │       │   │   │   │   │   ├── body1_walkEnd_anim.usd
│   │   │   │       │       │   │   │   │   │   ├── body1_walkLoop_anim.usd
│   │   │   │       │       │   │   │   │   │   └── body1_wave_anim.usd
│   │   │   │       │       │   │   │   │   ├── body2
│   │   │   │       │       │   │   │   │   │   ├── body2_celebrate_anim.usd
│   │   │   │       │       │   │   │   │   │   ├── body2_idle_anim.usd
│   │   │   │       │       │   │   │   │   │   ├── body2_walkEnd_anim.usd
│   │   │   │       │       │   │   │   │   │   ├── body2_walkLoop_anim.usd
│   │   │   │       │       │   │   │   │   │   └── body2_wave_anim.usd
│   │   │   │       │       │   │   │   │   └── body3
│   │   │   │       │       │   │   │   │       ├── body3_celebrate_anim.usd
│   │   │   │       │       │   │   │   │       ├── body3_idle_anim.usd
│   │   │   │       │       │   │   │   │       ├── body3_walkEnd_anim.usd
│   │   │   │       │       │   │   │   │       ├── body3_walkLoop_anim.usd
│   │   │   │       │       │   │   │   │       └── body3_wave_anim.usd
│   │   │   │       │       │   │   │   ├── mesh
│   │   │   │       │       │   │   │   │   ├── backpack1.usdz
│   │   │   │       │       │   │   │   │   ├── backpack2.usdz
│   │   │   │       │       │   │   │   │   ├── backpack3.usdz
│   │   │   │       │       │   │   │   │   ├── body1.usdz
│   │   │   │       │       │   │   │   │   ├── body2.usdz
│   │   │   │       │       │   │   │   │   ├── body3.usdz
│   │   │   │       │       │   │   │   │   ├── head1.usdz
│   │   │   │       │       │   │   │   │   ├── head2.usdz
│   │   │   │       │       │   │   │   │   └── head3.usdz
│   │   │   │       │       │   │   │   ├── sounds
│   │   │   │       │       │   │   │   │   └── scratch
│   │   │   │       │       │   │   │   │       ├── body1_walk_step1.mp3
│   │   │   │       │       │   │   │   │       └── body1_walk_step2.mp3
│   │   │   │       │       │   │   │   └── textures
│   │   │   │       │       │   │   │       ├── eyes
│   │   │   │       │       │   │   │       │   ├── eyes1_blink_anim.jpg
│   │   │   │       │       │   │   │       │   ├── eyes2_blink_anim.jpg
│   │   │   │       │       │   │   │       │   └── eyes3_blink_anim.jpg
│   │   │   │       │       │   │   │       ├── lights
│   │   │   │       │       │   │   │       │   ├── PB.jpg
│   │   │   │       │       │   │   │       │   ├── PB_2.jpg
│   │   │   │       │       │   │   │       │   ├── PB_3.jpg
│   │   │   │       │       │   │   │       │   ├── RB.jpg
│   │   │   │       │       │   │   │       │   ├── RB_2.jpg
│   │   │   │       │       │   │   │       │   ├── RB_3.jpg
│   │   │   │       │       │   │   │       │   └── stripes_Mask.jpg
│   │   │   │       │       │   │   │       ├── mesh
│   │   │   │       │       │   │   │       │   ├── backpack1
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_mesh_black.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_mesh_grey.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_mesh_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_mesh_yellow.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Metalness_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Normal_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Opacity_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_backpack1_Roughness_mesh_.jpg
│   │   │   │       │       │   │   │       │   ├── backpack2
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_mesh_black.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_mesh_grey.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_mesh_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_mesh_yellow.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Metalness_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Normal_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Opacity_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_backpack2_Roughness_mesh_.jpg
│   │   │   │       │       │   │   │       │   ├── backpack3
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_mesh_black.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_mesh_grey.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_mesh_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_mesh_yellow.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Metalness_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Normal_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Opacity_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_backpack3_Roughness_mesh_.jpg
│   │   │   │       │       │   │   │       │   ├── body1
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_mesh_black.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_mesh_grey.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_mesh_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_mesh_yellow.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_Normal_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_body1_Roughness_mesh_.jpg
│   │   │   │       │       │   │   │       │   ├── body2
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_mesh_black.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_mesh_grey.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_mesh_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_mesh_yellow.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_Normal_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_body2_Roughness_mesh_.jpg
│   │   │   │       │       │   │   │       │   ├── body3
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_mesh_black.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_mesh_grey.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_mesh_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_mesh_yellow.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_Normal_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_body3_Roughness_mesh_.jpg
│   │   │   │       │       │   │   │       │   ├── head1
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_mesh_black.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_mesh_grey.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_mesh_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_mesh_yellow.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_Normal_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_head1_Roughness_mesh_.jpg
│   │   │   │       │       │   │   │       │   ├── head2
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_mesh_black.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_mesh_grey.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_mesh_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_mesh_yellow.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_Normal_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_head2_Roughness_mesh_.jpg
│   │   │   │       │       │   │   │       │   └── head3
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_mesh_black.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_mesh_grey.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_mesh_orange.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_mesh_yellow.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_Normal_mesh_.jpg
│   │   │   │       │       │   │   │       │       └── T_head3_Roughness_mesh_.jpg
│   │   │   │       │       │   │   │       ├── metal
│   │   │   │       │       │   │   │       │   ├── backpack1
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_AmbientOcclusion_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_metal_blue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_metal_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_metal_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_metal_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Metalness_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Normal_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Opacity_metal_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_backpack1_Roughness_metal_.jpg
│   │   │   │       │       │   │   │       │   ├── backpack2
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_metal_blue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_metal_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_metal_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_metal_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Metalness_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Normal_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Opacity_metal_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_backpack2_Roughness_metal_.jpg
│   │   │   │       │       │   │   │       │   ├── backpack3
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_metal_blue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_metal_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_metal_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_metal_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Metalness_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Normal_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Opacity_metal_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_backpack3_Roughness_metal_.jpg
│   │   │   │       │       │   │   │       │   ├── body1
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_metal_blue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_metal_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_metal_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_metal_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_Metalness_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_Normal_metal_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_body1_Roughness_metal_.jpg
│   │   │   │       │       │   │   │       │   ├── body2
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_metal_blue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_metal_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_metal_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_metal_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_Metalness_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_Normal_metal_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_body2_Roughness_metal_.jpg
│   │   │   │       │       │   │   │       │   ├── body3
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_metal_blue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_metal_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_metal_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_metal_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_Metalness_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_Normal_metal_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_body3_Roughness_metal_.jpg
│   │   │   │       │       │   │   │       │   ├── head1
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_metal_blue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_metal_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_metal_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_metal_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_Normal_metal_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_head1_Roughness_metal_.jpg
│   │   │   │       │       │   │   │       │   ├── head2
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_metal_blue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_metal_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_metal_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_metal_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_Normal_metal_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_head2_Roughness_metal_.jpg
│   │   │   │       │       │   │   │       │   └── head3
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_metal_blue.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_metal_green.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_metal_orange.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_metal_pink.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_Normal_metal_.jpg
│   │   │   │       │       │   │   │       │       └── T_head3_Roughness_metal_.jpg
│   │   │   │       │       │   │   │       ├── plastic
│   │   │   │       │       │   │   │       │   ├── backpack1
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_plastic_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_plastic_lightBlue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_plastic_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_plastic_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Metalness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Normal_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Opacity_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Roughness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_backpack1_clearCoatMask_plastic_.jpg
│   │   │   │       │       │   │   │       │   ├── backpack2
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_plastic_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_plastic_lightBlue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_plastic_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_plastic_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Metalness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Normal_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Opacity_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Roughness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_backpack2_clearCoatMask_plastic_.jpg
│   │   │   │       │       │   │   │       │   ├── backpack3
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_plastic_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_plastic_lightBlue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_plastic_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_plastic_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Metalness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Normal_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Opacity_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Roughness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_backpack3_clearCoatMask_plastic_.jpg
│   │   │   │       │       │   │   │       │   ├── body1
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_plastic_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_plastic_lightBlue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_plastic_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_plastic_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_Normal_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_Roughness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_body1_clearCoatMask_plastic_.jpg
│   │   │   │       │       │   │   │       │   ├── body2
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_plastic_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_plastic_lightBlue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_plastic_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_plastic_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_Normal_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_Roughness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_body2_clearCoatMask_plastic_.jpg
│   │   │   │       │       │   │   │       │   ├── body3
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_plastic_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_plastic_lightBlue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_plastic_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_plastic_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_Normal_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_Roughness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_body3_clearCoatMask_plastic_.jpg
│   │   │   │       │       │   │   │       │   ├── head1
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_plastic_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_plastic_lightBlue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_plastic_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_plastic_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_Normal_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_Roughness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_head1_clearcoatMask_plastic_.jpg
│   │   │   │       │       │   │   │       │   ├── head2
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_plastic_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_plastic_lightBlue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_plastic_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_plastic_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_Normal_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_Roughness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_head2_clearCoatMask_plastic_.jpg
│   │   │   │       │       │   │   │       │   └── head3
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_plastic_green.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_plastic_lightBlue.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_plastic_orange.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_plastic_pink.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_Normal_plastic_.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_Roughness_plastic_.jpg
│   │   │   │       │       │   │   │       │       └── T_head3_clearCoatMask_plastic_.jpg
│   │   │   │       │       │   │   │       └── rainbow
│   │   │   │       │       │   │   │           ├── backpack1
│   │   │   │       │       │   │   │           │   ├── T_backpack1_BaseColor_rainbow_beige.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack1_BaseColor_rainbow_black.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack1_BaseColor_rainbow_red.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack1_BaseColor_rainbow_rose.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack1_Metalness_rainbow_.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack1_Normal_rainbow_.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack1_Opacity_rainbow_.jpg
│   │   │   │       │       │   │   │           │   └── T_backpack1_Roughness_rainbow_.jpg
│   │   │   │       │       │   │   │           ├── backpack2
│   │   │   │       │       │   │   │           │   ├── T_backpack2_BaseColor_rainbow_beige.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack2_BaseColor_rainbow_black.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack2_BaseColor_rainbow_red.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack2_BaseColor_rainbow_rose.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack2_Metalness_rainbow_.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack2_Normal_rainbow_.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack2_Opacity_rainbow_.jpg
│   │   │   │       │       │   │   │           │   └── T_backpack2_Roughness_rainbow_.jpg
│   │   │   │       │       │   │   │           ├── backpack3
│   │   │   │       │       │   │   │           │   ├── T_backpack3_BaseColor_rainbow_beige.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack3_BaseColor_rainbow_black.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack3_BaseColor_rainbow_red.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack3_BaseColor_rainbow_rose.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack3_Metalness_rainbow_.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack3_Normal_rainbow_.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack3_Opacity_rainbow_.jpg
│   │   │   │       │       │   │   │           │   └── T_backpack3_Roughness_rainbow_.jpg
│   │   │   │       │       │   │   │           ├── body1
│   │   │   │       │       │   │   │           │   ├── T_body1_BaseColor_rainbow_beige.jpg
│   │   │   │       │       │   │   │           │   ├── T_body1_BaseColor_rainbow_black.jpg
│   │   │   │       │       │   │   │           │   ├── T_body1_BaseColor_rainbow_red.jpg
│   │   │   │       │       │   │   │           │   ├── T_body1_BaseColor_rainbow_rose.jpg
│   │   │   │       │       │   │   │           │   ├── T_body1_Normal_rainbow_.jpg
│   │   │   │       │       │   │   │           │   └── T_body1_Roughness_rainbow_.jpg
│   │   │   │       │       │   │   │           ├── body2
│   │   │   │       │       │   │   │           │   ├── T_body2_BaseColor_rainbow_beige.jpg
│   │   │   │       │       │   │   │           │   ├── T_body2_BaseColor_rainbow_black.jpg
│   │   │   │       │       │   │   │           │   ├── T_body2_BaseColor_rainbow_red.jpg
│   │   │   │       │       │   │   │           │   ├── T_body2_BaseColor_rainbow_rose.jpg
│   │   │   │       │       │   │   │           │   ├── T_body2_Normal_rainbow_.jpg
│   │   │   │       │       │   │   │           │   └── T_body2_Roughness_rainbow_.jpg
│   │   │   │       │       │   │   │           ├── body3
│   │   │   │       │       │   │   │           │   ├── T_body3_BaseColor_rainbow_beige.jpg
│   │   │   │       │       │   │   │           │   ├── T_body3_BaseColor_rainbow_black.jpg
│   │   │   │       │       │   │   │           │   ├── T_body3_BaseColor_rainbow_red.jpg
│   │   │   │       │       │   │   │           │   ├── T_body3_BaseColor_rainbow_rose.jpg
│   │   │   │       │       │   │   │           │   ├── T_body3_Normal_rainbow_.jpg
│   │   │   │       │       │   │   │           │   └── T_body3_Roughness_rainbow_.jpg
│   │   │   │       │       │   │   │           ├── head1
│   │   │   │       │       │   │   │           │   ├── T_head1_BaseColor_rainbow_beige.jpg
│   │   │   │       │       │   │   │           │   ├── T_head1_BaseColor_rainbow_black.jpg
│   │   │   │       │       │   │   │           │   ├── T_head1_BaseColor_rainbow_red.jpg
│   │   │   │       │       │   │   │           │   ├── T_head1_BaseColor_rainbow_rose.jpg
│   │   │   │       │       │   │   │           │   ├── T_head1_Normal_rainbow_.jpg
│   │   │   │       │       │   │   │           │   └── T_head1_Roughness_rainbow_.jpg
│   │   │   │       │       │   │   │           ├── head2
│   │   │   │       │       │   │   │           │   ├── T_head2_BaseColor_rainbow_beige.jpg
│   │   │   │       │       │   │   │           │   ├── T_head2_BaseColor_rainbow_black.jpg
│   │   │   │       │       │   │   │           │   ├── T_head2_BaseColor_rainbow_red.jpg
│   │   │   │       │       │   │   │           │   ├── T_head2_BaseColor_rainbow_rose.jpg
│   │   │   │       │       │   │   │           │   ├── T_head2_Normal_rainbow_.jpg
│   │   │   │       │       │   │   │           │   └── T_head2_Roughness_rainbow_.jpg
│   │   │   │       │       │   │   │           └── head3
│   │   │   │       │       │   │   │               ├── T_head3_BaseColor_rainbow_beige.jpg
│   │   │   │       │       │   │   │               ├── T_head3_BaseColor_rainbow_black.jpg
│   │   │   │       │       │   │   │               ├── T_head3_BaseColor_rainbow_red.jpg
│   │   │   │       │       │   │   │               ├── T_head3_BaseColor_rainbow_rose.jpg
│   │   │   │       │       │   │   │               ├── T_head3_Normal_rainbow_.jpg
│   │   │   │       │       │   │   │               └── T_head3_Roughness_rainbow_.jpg
│   │   │   │       │       │   │   ├── environment
│   │   │   │       │       │   │   │   ├── mesh
│   │   │   │       │       │   │   │   │   └── volume.usd
│   │   │   │       │       │   │   │   └── textures
│   │   │   │       │       │   │   │       ├── T_dirt_AmbientOcclusion.jpg
│   │   │   │       │       │   │   │       ├── T_dirt_BaseColor.jpg
│   │   │   │       │       │   │   │       ├── T_dirt_Height.jpg
│   │   │   │       │       │   │   │       ├── T_dirt_Normal.jpg
│   │   │   │       │       │   │   │       ├── T_dirt_Roughness.jpg
│   │   │   │       │       │   │   │       ├── T_islandBase_BaseColor.jpg
│   │   │   │       │       │   │   │       ├── T_islandBase_Normal.jpg
│   │   │   │       │       │   │   │       ├── T_islandBase_Roughness.jpg
│   │   │   │       │       │   │   │       ├── T_islandEdge_BaseColor.jpg
│   │   │   │       │       │   │   │       ├── T_islandEdge_Metalness.jpg
│   │   │   │       │       │   │   │       ├── T_islandEdge_Normal.jpg
│   │   │   │       │       │   │   │       ├── T_islandEdge_Roughness.jpg
│   │   │   │       │       │   │   │       ├── T_islandTop_BaseColor.jpg
│   │   │   │       │       │   │   │       ├── T_islandTop_Normal.jpg
│   │   │   │       │       │   │   │       ├── T_islandTop_Roughness.jpg
│   │   │   │       │       │   │   │       ├── T_planters_BaseColor.jpg
│   │   │   │       │       │   │   │       ├── T_planters_Metalness.jpg
│   │   │   │       │       │   │   │       ├── T_planters_Normal.jpg
│   │   │   │       │       │   │   │       ├── T_planters_Roughness.jpg
│   │   │   │       │       │   │   │       └── T_planters_circle_mask.jpg
│   │   │   │       │       │   │   └── plants
│   │   │   │       │       │   │       ├── animations
│   │   │   │       │       │   │       │   ├── coffeeBerry_celebrate_anim.usdz
│   │   │   │       │       │   │       │   ├── coffeeBerry_grow_anim.usdz
│   │   │   │       │       │   │       │   ├── poppy_celebrate_anim.usdz
│   │   │   │       │       │   │       │   ├── poppy_grow_anim.usdz
│   │   │   │       │       │   │       │   ├── yucca_celebrate_anim.usdz
│   │   │   │       │       │   │       │   └── yucca_grow_anim.usdz
│   │   │   │       │       │   │       ├── mesh
│   │   │   │       │       │   │       │   ├── hero
│   │   │   │       │       │   │       │   │   ├── coffeeBerry.usdz
│   │   │   │       │       │   │       │   │   ├── poppy.usdz
│   │   │   │       │       │   │       │   │   └── yucca.usdz
│   │   │   │       │       │   │       │   └── setDressing
│   │   │   │       │       │   │       │       ├── bottomSetDressing.usd
│   │   │   │       │       │   │       │       └── foliageSetDressing.usd
│   │   │   │       │       │   │       └── textures
│   │   │   │       │       │   │           ├── T_bigPlant_BaseColor.jpg
│   │   │   │       │       │   │           ├── T_bigPlant_Emissive.jpg
│   │   │   │       │       │   │           ├── T_bigPlant_Normal.jpg
│   │   │   │       │       │   │           ├── T_bigPlant_Roughness.jpg
│   │   │   │       │       │   │           ├── T_bigPlant_bulb_mask.jpg
│   │   │   │       │       │   │           ├── T_bigPlant_emissive2_mask.jpg
│   │   │   │       │       │   │           ├── T_bigPlant_emissive_mask.jpg
│   │   │   │       │       │   │           ├── T_coffeeBerry_BaseColor.jpg
│   │   │   │       │       │   │           ├── T_coffeeBerry_Emissive.jpg
│   │   │   │       │       │   │           ├── T_coffeeBerry_Normal.jpg
│   │   │   │       │       │   │           ├── T_coffeeBerry_Roughness.jpg
│   │   │   │       │       │   │           ├── T_coffeeBerry_berry_mask.jpg
│   │   │   │       │       │   │           ├── T_coffeeberry_upLight_mask.jpg
│   │   │   │       │       │   │           ├── T_poppy_BaseColor.jpg
│   │   │   │       │       │   │           ├── T_poppy_Emissive.jpg
│   │   │   │       │       │   │           ├── T_poppy_Mask.jpg
│   │   │   │       │       │   │           ├── T_poppy_Normal.jpg
│   │   │   │       │       │   │           ├── T_poppy_Roughness.jpg
│   │   │   │       │       │   │           ├── T_poppy_emissiveMask.jpg
│   │   │   │       │       │   │           ├── T_poppy_upLight_mask.jpg
│   │   │   │       │       │   │           ├── T_sidePlant_BaseColor.jpg
│   │   │   │       │       │   │           ├── T_sidePlant_Normal.jpg
│   │   │   │       │       │   │           ├── T_sidePlant_Roughness.jpg
│   │   │   │       │       │   │           ├── T_sidePlant_curvature_mask.jpg
│   │   │   │       │       │   │           ├── T_sidePlant_emissive_mask.jpg
│   │   │   │       │       │   │           ├── T_yucca_BaseColor.jpg
│   │   │   │       │       │   │           ├── T_yucca_Emissive.jpg
│   │   │   │       │       │   │           ├── T_yucca_Normal.jpg
│   │   │   │       │       │   │           ├── T_yucca_Roughness.jpg
│   │   │   │       │       │   │           ├── T_yucca_emissive_mask.jpg
│   │   │   │       │       │   │           ├── T_yucca_upLight_mask.jpg
│   │   │   │       │       │   │           ├── poppyThickness_mask.jpg
│   │   │   │       │       │   │           └── sideplant_EmmissiveMask.jpg
│   │   │   │       │       │   ├── Materials
│   │   │   │       │       │   │   ├── M_environment.usda
│   │   │   │       │       │   │   ├── M_face.usda
│   │   │   │       │       │   │   ├── M_lights.usda
│   │   │   │       │       │   │   ├── M_mesh.usda
│   │   │   │       │       │   │   ├── M_metal.usda
│   │   │   │       │       │   │   ├── M_plants.usda
│   │   │   │       │       │   │   ├── M_plastic.usda
│   │   │   │       │       │   │   └── M_rainbow.usda
│   │   │   │       │       │   └── scenes
│   │   │   │       │       │       ├── backpack1.usda
│   │   │   │       │       │       ├── backpack2.usda
│   │   │   │       │       │       ├── backpack3.usda
│   │   │   │       │       │       ├── body1.usda
│   │   │   │       │       │       ├── body2.usda
│   │   │   │       │       │       ├── body3.usda
│   │   │   │       │       │       ├── head1.usda
│   │   │   │       │       │       ├── head2.usda
│   │   │   │       │       │       ├── head3.usda
│   │   │   │       │       │       ├── lighting.usda
│   │   │   │       │       │       ├── planter_Hero.usda
│   │   │   │       │       │       ├── setDressing.usda
│   │   │   │       │       │       └── volume.usda
│   │   │   │       │       ├── Components
│   │   │   │       │       │   └── PlantComponent.swift
│   │   │   │       │       ├── Extensions
│   │   │   │       │       │   └── EntityExtensions.swift
│   │   │   │       │       └── BOTanistAssets.swift
│   │   │   │       └── Package.swift
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── BuildingLocalExperiencesWithRoomTracking
│   │   │   ├── ARKitRoomTracking
│   │   │   │   ├── ARKitRoomTrackingApp.swift
│   │   │   │   ├── AppState.swift
│   │   │   │   ├── ContentView.swift
│   │   │   │   ├── Extensions.swift
│   │   │   │   ├── Info.plist
│   │   │   │   └── WorldAndRoomView.swift
│   │   │   ├── ARKitRoomTracking.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── ARKitRoomTracking.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── Combining2DAnd3DViewsInAnImmersiveApp
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── MultiDimensionalImmersiveContent
│   │   │   │   ├── Assets.xcassets
│   │   │   │   │   ├── AppIcon.appiconset
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   └── Contents.json
│   │   │   │   ├── CALayerArch
│   │   │   │   │   ├── CALayerArcRepresentable.swift
│   │   │   │   │   └── CALayerArcView.swift
│   │   │   │   ├── Preview Content
│   │   │   │   │   └── Preview Assets.xcassets
│   │   │   │   │       └── Contents.json
│   │   │   │   ├── SwiftUIArch
│   │   │   │   │   └── SwiftUIArcView.swift
│   │   │   │   ├── UIViewArch
│   │   │   │   │   ├── UIViewArcRepresentable.swift
│   │   │   │   │   └── UIViewArcView.swift
│   │   │   │   ├── Extensions.swift
│   │   │   │   ├── Info.plist
│   │   │   │   ├── MultiDimensionalImmersiveContentApp.swift
│   │   │   │   ├── RainbowModel.swift
│   │   │   │   └── RainbowView.swift
│   │   │   ├── MultiDimensionalImmersiveContent.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── MultiDimensionalImmersiveContent.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── Packages
│   │   │   │   └── RealityKitContent
│   │   │   │       ├── Package.realitycomposerpro
│   │   │   │       │   ├── Library
│   │   │   │       │   ├── PluginData
│   │   │   │       │   ├── ProjectData
│   │   │   │       │   │   └── main.json
│   │   │   │       │   └── WorkspaceData
│   │   │   │       │       ├── SceneMetadataList.json
│   │   │   │       │       └── Settings.rcprojectdata
│   │   │   │       ├── Sources
│   │   │   │       │   └── RealityKitContent
│   │   │   │       │       ├── RealityKitContent.rkassets
│   │   │   │       │       │   ├── Materials
│   │   │   │       │       │   │   └── GreenMaterial.usda
│   │   │   │       │       │   ├── green.usdc
│   │   │   │       │       │   ├── plane.usdc
│   │   │   │       │       │   └── yellow.usdc
│   │   │   │       │       └── RealityKitContent.swift
│   │   │   │       ├── Package.swift
│   │   │   │       └── README.md
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── Creating2DShapesInVisionOSWithSwiftUI
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── Creating 2D Shapes
│   │   │   │   ├── Assets.xcassets
│   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   └── Contents.json
│   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   └── Contents.json
│   │   │   │   ├── EntryPoint.swift
│   │   │   │   ├── Info.plist
│   │   │   │   ├── Line.swift
│   │   │   │   ├── MainView.swift
│   │   │   │   ├── ShapesView.swift
│   │   │   │   └── Triangle.swift
│   │   │   ├── Creating 2D Shapes.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── Creating3DEntitiesInVisionOSWithRealityKit
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── Creating 3D Shapes
│   │   │   │   ├── App
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── EntryPoint.swift
│   │   │   │   │   └── Info.plist
│   │   │   │   ├── Entities
│   │   │   │   │   └── ShapesView+Entities.swift
│   │   │   │   └── Views
│   │   │   │       └── ShapesView.swift
│   │   │   ├── Creating 3D Shapes.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── 3D Shapes.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── CreatingA3DModelWithGesturesInVisionOS
│   │   │   ├── CarExample
│   │   │   │   ├── App
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── EntryPoint.swift
│   │   │   │   │   └── Info.plist
│   │   │   │   ├── Extensions
│   │   │   │   │   └── SIMD3.swift
│   │   │   │   ├── Resources
│   │   │   │   │   └── Huracan-EVO-RWD-Spyder-opt-22.usdz
│   │   │   │   └── Views
│   │   │   │       ├── CarView.swift
│   │   │   │       └── MainView.swift
│   │   │   ├── CarExample.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── CreatingA3DPaintingSpaceInVisionOS
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── Painting
│   │   │   │   ├── App
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── EntryPoint.swift
│   │   │   │   │   └── Info.plist
│   │   │   │   ├── Canvas
│   │   │   │   │   ├── PaintingCanvas.swift
│   │   │   │   │   └── Stroke.swift
│   │   │   │   ├── Components
│   │   │   │   │   └── ClosureComponent.swift
│   │   │   │   ├── Extensions
│   │   │   │   │   ├── Entity.swift
│   │   │   │   │   └── Float.swift
│   │   │   │   ├── Trackers
│   │   │   │   │   └── PaintingHandTracking.swift
│   │   │   │   └── Views
│   │   │   │       ├── MainView.swift
│   │   │   │       └── PaintingView.swift
│   │   │   ├── Painting.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── CreatingANewSwiftUIWindowViewInVisionOS
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── Creating New Windows
│   │   │   │   ├── App
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── EntryPoint.swift
│   │   │   │   │   └── Info.plist
│   │   │   │   └── Views
│   │   │   │       ├── MainView.swift
│   │   │   │       ├── NewWindowView.swift
│   │   │   │       └── OpenWindowView.swift
│   │   │   ├── Creating New Windows.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── CreatingAVolumetricWindowInVisionOS
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── Creating a Volumetric Window
│   │   │   │   ├── App
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── EntryPoint.swift
│   │   │   │   │   └── Info.plist
│   │   │   │   ├── Resources
│   │   │   │   │   └── cup_saucer_set.usdz
│   │   │   │   └── Views
│   │   │   │       └── VolumetricWindow.swift
│   │   │   ├── Creating a Volumetric Window.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── Volumetric Window.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── CreatingGlassMaterialFor3DShapesInVisionOS
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── Glass
│   │   │   │   ├── App
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── EntryPoint.swift
│   │   │   │   │   └── Info.plist
│   │   │   │   ├── Extentions
│   │   │   │   │   └── Entity.swift
│   │   │   │   ├── Resources
│   │   │   │   │   ├── Dragon.usdc
│   │   │   │   │   └── DragonGlass.usda
│   │   │   │   └── Views
│   │   │   │       ├── GlassView.swift
│   │   │   │       └── MainView.swift
│   │   │   ├── Glass.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── CreatingImmersiveSpacesInVisionOSWithSwiftUI
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── Creating Immersive Spaces
│   │   │   │   ├── App
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── EntryPoint.swift
│   │   │   │   │   └── Info.plist
│   │   │   │   ├── Extensions
│   │   │   │   │   └── Entity.swift
│   │   │   │   ├── Resources
│   │   │   │   │   └── rock.usdz
│   │   │   │   ├── Systems
│   │   │   │   │   └── TurnTableSystem.swift
│   │   │   │   └── Views
│   │   │   │       ├── ImmersionView.swift
│   │   │   │       └── MainView.swift
│   │   │   ├── Creating Immersive Spaces.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── DestinationVideo
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── DestinationVideo
│   │   │   │   ├── Extensions
│   │   │   │   │   ├── AVExtensions.swift
│   │   │   │   │   ├── DestinationVideoExtensions.swift
│   │   │   │   │   └── MultiplatformExtensions.swift
│   │   │   │   ├── Model
│   │   │   │   │   ├── Data
│   │   │   │   │   │   ├── Genre.swift
│   │   │   │   │   │   ├── Importer.swift
│   │   │   │   │   │   ├── Person.swift
│   │   │   │   │   │   ├── PreviewData.swift
│   │   │   │   │   │   ├── RelationshipMapping.swift
│   │   │   │   │   │   ├── SampleData.swift
│   │   │   │   │   │   ├── UpNextItem.swift
│   │   │   │   │   │   └── Video.swift
│   │   │   │   │   ├── visionOS
│   │   │   │   │   │   ├── EnvironmentStateHandler.swift
│   │   │   │   │   │   └── ImmersiveEnvironment.swift
│   │   │   │   │   ├── Category.swift
│   │   │   │   │   ├── Constants.swift
│   │   │   │   │   ├── NavigationNode.swift
│   │   │   │   │   └── Tabs.swift
│   │   │   │   ├── Player
│   │   │   │   │   ├── InlinePlayerView.swift
│   │   │   │   │   ├── PlayerModel.swift
│   │   │   │   │   ├── PlayerView.swift
│   │   │   │   │   ├── SystemPlayerView.swift
│   │   │   │   │   └── UpNextView.swift
│   │   │   │   ├── Preview Content
│   │   │   │   │   └── Preview Assets.xcassets
│   │   │   │   │       └── Contents.json
│   │   │   │   ├── Resources
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AccentColor.colorset
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── AppIcon.appiconset
│   │   │   │   │   │   │   ├── AppIcon.png
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   ├── DarkAppIcon.png
│   │   │   │   │   │   │   ├── TintableAppIcon.png
│   │   │   │   │   │   │   ├── icon_128x128.png
│   │   │   │   │   │   │   ├── icon_128x128@2x.png
│   │   │   │   │   │   │   ├── icon_16x16.png
│   │   │   │   │   │   │   ├── icon_16x16@2x.png
│   │   │   │   │   │   │   ├── icon_256x256.png
│   │   │   │   │   │   │   ├── icon_256x256@2x.png
│   │   │   │   │   │   │   ├── icon_32x32.png
│   │   │   │   │   │   │   ├── icon_32x32@2x.png
│   │   │   │   │   │   │   ├── icon_512x512.png
│   │   │   │   │   │   │   └── icon_512x512@2x.png
│   │   │   │   │   │   ├── AppIcon.brandassets
│   │   │   │   │   │   │   ├── App Icon - App Store.imagestack
│   │   │   │   │   │   │   │   ├── Back.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   ├── Front.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   ├── Middle.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── App Icon.imagestack
│   │   │   │   │   │   │   │   ├── Back.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   ├── Back.png
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   ├── Front.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   │   │   └── Front.png
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   ├── Middle.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Top Shelf Image Wide.imageset
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Top Shelf Image.imageset
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   ├── Back.png
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   │   └── Front.png
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── BOT-anist_landscape.imageset
│   │   │   │   │   │   │   ├── BOT-anist_landscape.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── BOT-anist_portrait.imageset
│   │   │   │   │   │   │   ├── BOT-anist_portrait.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── amazing_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── amazing-animation-poster.png
│   │   │   │   │   │   ├── animals_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── cute-animals-poster.png
│   │   │   │   │   │   ├── beach_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── beach_landscape.png
│   │   │   │   │   │   ├── beach_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── beach_portrait.png
│   │   │   │   │   │   ├── camping_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── camping_landscape.png
│   │   │   │   │   │   ├── camping_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── camping_portrait.png
│   │   │   │   │   │   ├── cinematic_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── cinematic_poster.png
│   │   │   │   │   │   ├── creek_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── creek_landscape.png
│   │   │   │   │   │   ├── creek_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── creek_portrait.png
│   │   │   │   │   │   ├── dance_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── dance_landscape.png
│   │   │   │   │   │   ├── dance_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── dance_portrait.png
│   │   │   │   │   │   ├── discovery_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── discovery_landscape.png
│   │   │   │   │   │   ├── discovery_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── discovery_portrait.png
│   │   │   │   │   │   ├── dv_logo.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── dv_logo@2x.png
│   │   │   │   │   │   ├── extraordinary_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── extraordinary-poster.png
│   │   │   │   │   │   ├── forest_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── forest_poster.png
│   │   │   │   │   │   ├── hillside_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── hillside_landscape.png
│   │   │   │   │   │   ├── hillside_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── hillside_portrait.png
│   │   │   │   │   │   ├── lab_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── lab_landscape.png
│   │   │   │   │   │   ├── lab_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── lab_portrait.png
│   │   │   │   │   │   ├── lake_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── lake_landscape.png
│   │   │   │   │   │   ├── lake_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── lake_portrait.png
│   │   │   │   │   │   ├── landing_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── landing_landscape.png
│   │   │   │   │   │   ├── landing_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── landing_portriat.png
│   │   │   │   │   │   ├── ocean_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── ocean_landscape.png
│   │   │   │   │   │   ├── ocean_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── ocean_portrait.png
│   │   │   │   │   │   ├── park_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── park_landscape.png
│   │   │   │   │   │   ├── park_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── park_portrait.png
│   │   │   │   │   │   ├── samples_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── samples_landscape.png
│   │   │   │   │   │   ├── samples_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── samples_portriat.png
│   │   │   │   │   │   ├── sea_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── by-the-sea-poster.png
│   │   │   │   │   │   ├── studio_thumbnail_dark.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── studio_thumbnail_dark.png
│   │   │   │   │   │   ├── studio_thumbnail_light.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── studio_thumbnail_light.png
│   │   │   │   │   │   ├── tvBackground.colorset
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Videos
│   │   │   │   │   │   ├── BOT-anist_video.mov
│   │   │   │   │   │   └── dance_video.mov
│   │   │   │   │   ├── de.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── fr.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── hi.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── ja.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── ko.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── zh_CN.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   └── Localizable.xcstrings
│   │   │   │   ├── SharePlay
│   │   │   │   │   ├── WatchingActivity.swift
│   │   │   │   │   └── WatchingCoordinator.swift
│   │   │   │   ├── Views
│   │   │   │   │   ├── visionOS
│   │   │   │   │   │   ├── ImmersiveEnvironmentPickerView.swift
│   │   │   │   │   │   ├── ImmersiveEnvironmentView.swift
│   │   │   │   │   │   ├── ProfileButton.swift
│   │   │   │   │   │   └── TrailerView.swift
│   │   │   │   │   ├── ButtonStyle.swift
│   │   │   │   │   ├── CategoryListView.swift
│   │   │   │   │   ├── CategoryView.swift
│   │   │   │   │   ├── DetailView.swift
│   │   │   │   │   ├── GradientView.swift
│   │   │   │   │   ├── HeroView.swift
│   │   │   │   │   ├── LibraryView.swift
│   │   │   │   │   ├── VideoCardView.swift
│   │   │   │   │   ├── VideoInfoView.swift
│   │   │   │   │   ├── VideoListView.swift
│   │   │   │   │   ├── ViewModifiers.swift
│   │   │   │   │   └── WatchNowView.swift
│   │   │   │   ├── ContentView.swift
│   │   │   │   ├── DestinationTabs.swift
│   │   │   │   ├── DestinationVideo.entitlements
│   │   │   │   ├── DestinationVideo.swift
│   │   │   │   ├── Info.plist
│   │   │   │   └── PlayerWindow.swift
│   │   │   ├── DestinationVideo.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── Packages
│   │   │   │   └── Studio
│   │   │   │       ├── Package.realitycomposerpro
│   │   │   │       │   ├── ProjectData
│   │   │   │       │   │   └── main.json
│   │   │   │       │   └── WorkspaceData
│   │   │   │       │       ├── SceneMetadataList.json
│   │   │   │       │       └── Settings.rcprojectdata
│   │   │   │       ├── Sources
│   │   │   │       │   └── Studio
│   │   │   │       │       ├── Studio.rkassets
│   │   │   │       │       │   ├── ibl
│   │   │   │       │       │   │   ├── Studio_IBL_LatLong_Dark.exr
│   │   │   │       │       │   │   └── Studio_IBL_LatLong_Light.exr
│   │   │   │       │       │   ├── meshes
│   │   │   │       │       │   │   ├── Studio.usdc
│   │   │   │       │       │   │   ├── Studio_floor_2_2_Lightspill.usdc
│   │   │   │       │       │   │   ├── Studio_floor_2_Lightspill.usdc
│   │   │   │       │       │   │   └── dome.usdc
│   │   │   │       │       │   ├── scenes
│   │   │   │       │       │   │   ├── Common.usda
│   │   │   │       │       │   │   ├── Floor.usda
│   │   │   │       │       │   │   ├── StudioDark.usda
│   │   │   │       │       │   │   └── StudioLight.usda
│   │   │   │       │       │   ├── textures
│   │   │   │       │       │   │   ├── common
│   │   │   │       │       │   │   │   └── DefaultAttenuationMap.exr
│   │   │   │       │       │   │   ├── dark
│   │   │   │       │       │   │   │   ├── BakingGroup1_1_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup1_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup2_2_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup2_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup3_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup4_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup5_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup6_d.png
│   │   │   │       │       │   │   │   └── BakingGroup7_d.png
│   │   │   │       │       │   │   ├── light
│   │   │   │       │       │   │   │   ├── BakingGroup1.png
│   │   │   │       │       │   │   │   ├── BakingGroup1_1.png
│   │   │   │       │       │   │   │   ├── BakingGroup2.png
│   │   │   │       │       │   │   │   ├── BakingGroup2_2.png
│   │   │   │       │       │   │   │   ├── BakingGroup3.png
│   │   │   │       │       │   │   │   ├── BakingGroup4.png
│   │   │   │       │       │   │   │   ├── BakingGroup5.png
│   │   │   │       │       │   │   │   ├── BakingGroup6.png
│   │   │   │       │       │   │   │   └── BakingGroup7.png
│   │   │   │       │       │   │   └── skies
│   │   │   │       │       │   │       ├── Studio_sky_LatLong_Dark.exr
│   │   │   │       │       │   │       └── Studio_sky_LatLong_Light.exr
│   │   │   │       │       │   └── AAA_MainScene.usda
│   │   │   │       │       └── Studio.swift
│   │   │   │       └── Package.swift
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── DisplayingA3DObjectThatMovesToStayInAPersonsView
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── HeadTracking
│   │   │   │   ├── App
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── EntryPoint.swift
│   │   │   │   │   └── Info.plist
│   │   │   │   ├── Extensions
│   │   │   │   │   └── Floats.swift
│   │   │   │   ├── Systems
│   │   │   │   │   └── ClosureComponent.swift
│   │   │   │   ├── Tracker
│   │   │   │   │   └── HeadPositionTracker.swift
│   │   │   │   └── Views
│   │   │   │       ├── HeadPositionView.swift
│   │   │   │       └── MainView.swift
│   │   │   ├── HeadTracking.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── DisplayingTextInVisionOS
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── Text
│   │   │   │   ├── App
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Info.plist
│   │   │   │   │   └── TextApp.swift
│   │   │   │   └── Views
│   │   │   │       ├── MainView.swift
│   │   │   │       └── TextView.swift
│   │   │   ├── Text.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── ExploringObjectTrackingWithARKit
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── ObjectTracking
│   │   │   │   ├── App
│   │   │   │   │   ├── AppState.swift
│   │   │   │   │   ├── ObjectAnchorVisualization.swift
│   │   │   │   │   └── ReferenceObjectLoader.swift
│   │   │   │   ├── Extensions
│   │   │   │   │   └── Entity+ObjectTracking.swift
│   │   │   │   ├── Views
│   │   │   │   │   ├── HomeView.swift
│   │   │   │   │   ├── InfoLabel.swift
│   │   │   │   │   ├── ListEntryView.swift
│   │   │   │   │   └── ObjectTrackingRealityView.swift
│   │   │   │   ├── Info.plist
│   │   │   │   └── ObjectTrackingApp.swift
│   │   │   ├── ObjectTracking.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── ObjectTracking.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── Reference Objects
│   │   │   │   └── Apple_Magic_Keyboard.referenceobject
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── GeneratingProceduralTexturesInVisionOS
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── RealityKit-Drawable
│   │   │   │   ├── App
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Drawable.swift
│   │   │   │   │   └── Info.plist
│   │   │   │   ├── Resources
│   │   │   │   │   └── Torus.usda
│   │   │   │   ├── Systems
│   │   │   │   │   ├── DrawableQueueComponent.swift
│   │   │   │   │   └── DrawableQueueSystem.swift
│   │   │   │   ├── Textures
│   │   │   │   │   ├── DynamicTextureShaders.metal
│   │   │   │   │   └── ProceduralTextureGenerator.swift
│   │   │   │   └── Views
│   │   │   │       ├── DrawableView.swift
│   │   │   │       └── EntityView.swift
│   │   │   ├── RealityKit-Drawable.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── HappyBeam
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── HappyBeam
│   │   │   │   ├── Assets.xcassets
│   │   │   │   │   ├── AccentColor.colorset
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   ├── Bottom Layer@2x.png
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   └── topLayer@2x.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── finish-clouds.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── finish-clouds.png
│   │   │   │   │   ├── gesture_hand.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── gesture_hand.svg
│   │   │   │   │   ├── greatJob.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── greatJob@2x.png
│   │   │   │   │   ├── hands-diagram.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── hands-diagram.png
│   │   │   │   │   ├── keyboardGameController.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── keyboardGameController.svg
│   │   │   │   │   ├── shareplayGraphic.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── shareplayGraphic@2x.png
│   │   │   │   │   ├── splashScreen.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── splashScreenGraphic@2x.png
│   │   │   │   │   └── Contents.json
│   │   │   │   ├── Gameplay
│   │   │   │   │   ├── BeamCollisions.swift
│   │   │   │   │   ├── Clouds.swift
│   │   │   │   │   ├── HeartGestureModel.swift
│   │   │   │   │   ├── Multiplayer.swift
│   │   │   │   │   └── Players.swift
│   │   │   │   ├── Preview Content
│   │   │   │   │   └── Preview Assets.xcassets
│   │   │   │   │       └── Contents.json
│   │   │   │   ├── Sounds
│   │   │   │   │   ├── cloudHit1.m4a
│   │   │   │   │   ├── cloudHit2.m4a
│   │   │   │   │   ├── cloudHit3.m4a
│   │   │   │   │   ├── cloudHit4.m4a
│   │   │   │   │   ├── happyBeamGameplay.m4a
│   │   │   │   │   ├── happyBeamMenu.m4a
│   │   │   │   │   └── happyBeamVictory.m4a
│   │   │   │   ├── USDZs
│   │   │   │   │   ├── UpdatedGrumpyScene2.usdz
│   │   │   │   │   ├── cloud.usdz
│   │   │   │   │   └── fireworks.usdz
│   │   │   │   ├── Views
│   │   │   │   │   ├── HappyBeam.swift
│   │   │   │   │   ├── Lobby.swift
│   │   │   │   │   ├── MultiPlay.swift
│   │   │   │   │   ├── MultiScore.swift
│   │   │   │   │   ├── SoloPlay.swift
│   │   │   │   │   ├── SoloScore.swift
│   │   │   │   │   └── Start.swift
│   │   │   │   ├── Extensions.swift
│   │   │   │   ├── GameModel.swift
│   │   │   │   ├── GlobalEntities.swift
│   │   │   │   ├── HappyBeam.entitlements
│   │   │   │   ├── HappyBeamApp.swift
│   │   │   │   ├── HappyBeamSpace.swift
│   │   │   │   ├── Info.plist
│   │   │   │   ├── InfoPlist.xcstrings
│   │   │   │   └── Localizable.xcstrings
│   │   │   ├── HappyBeam.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── HappyBeam.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── Packages
│   │   │   │   └── HappyBeamAssets
│   │   │   │       ├── Package.realitycomposerpro
│   │   │   │       │   ├── ProjectData
│   │   │   │       │   │   └── main.json
│   │   │   │       │   └── WorkspaceData
│   │   │   │       │       ├── SceneMetadataList.json
│   │   │   │       │       └── Settings.rcprojectdata
│   │   │   │       ├── Sources
│   │   │   │       │   └── HappyBeamAssets
│   │   │   │       │       ├── HappyBeamAssets.rkassets
│   │   │   │       │       │   ├── UpdatedGrumpyScene2
│   │   │   │       │       │   │   ├── 0
│   │   │   │       │       │   │   │   ├── M_cloud_body_baseColor.jpg
│   │   │   │       │       │   │   │   ├── M_cloud_body_emmissive.jpg
│   │   │   │       │       │   │   │   ├── M_cloud_body_normal.png
│   │   │   │       │       │   │   │   ├── M_cloud_body_occlusion.jpg
│   │   │   │       │       │   │   │   ├── M_cloud_body_roughness.jpg
│   │   │   │       │       │   │   │   ├── M_cloud_face_baseColor.jpg
│   │   │   │       │       │   │   │   ├── cloud_002_anim.usdz
│   │   │   │       │       │   │   │   ├── happyClouds_baseColor_1.png
│   │   │   │       │       │   │   │   ├── m_happyCloud_face_normal_1.png
│   │   │   │       │       │   │   │   └── m_happyCloud_face_roughness_1.jpg
│   │   │   │       │       │   │   ├── UpdatedGrumpyScene2.usdc
│   │   │   │       │       │   │   └── cloud_lod1_anim_001_2-10.usdc
│   │   │   │       │       │   ├── textures
│   │   │   │       │       │   │   ├── heartBeam_basecolor_1.png
│   │   │   │       │       │   │   ├── heartBeam_metallic_1.jpg
│   │   │   │       │       │   │   ├── heartBeam_normal_1.png
│   │   │   │       │       │   │   ├── heartBeam_roughness_1.jpg
│   │   │   │       │       │   │   ├── heartLight_M_heartLight_baseColor 1.png
│   │   │   │       │       │   │   ├── heartLight_M_heartLight_baseColor.png
│   │   │   │       │       │   │   ├── heartLight_M_heartLight_metallic 1.jpg
│   │   │   │       │       │   │   ├── heartLight_M_heartLight_metallic.jpg
│   │   │   │       │       │   │   ├── heartLight_M_heartLight_normal 1.png
│   │   │   │       │       │   │   ├── heartLight_M_heartLight_normal.png
│   │   │   │       │       │   │   ├── heartLight_M_heartLight_roughness 1.jpg
│   │   │   │       │       │   │   ├── heartLight_M_heartLight_roughness.jpg
│   │   │   │       │       │   │   ├── mat_heart_Base_color_1.png
│   │   │   │       │       │   │   ├── mat_heart_Metallic_1.png
│   │   │   │       │       │   │   ├── mat_heart_Normal_1.png
│   │   │   │       │       │   │   └── mat_heart_Roughness_1.png
│   │   │   │       │       │   ├── Cloud.usda
│   │   │   │       │       │   ├── Heart.usda
│   │   │   │       │       │   ├── HeartBeam.usd
│   │   │   │       │       │   ├── HeartBlaster.usda
│   │   │   │       │       │   ├── HeartTurret.usda
│   │   │   │       │       │   ├── M_heartTurret_baseColor_1.png
│   │   │   │       │       │   ├── M_heartTurret_metallic_1.jpg
│   │   │   │       │       │   ├── M_heartTurret_normal_1.png
│   │   │   │       │       │   ├── M_heartTurret_roughness_1.jpg
│   │   │   │       │       │   ├── UpdatedGrumpyScene2.usdz
│   │   │   │       │       │   ├── heartBeam_basecolor_1.png
│   │   │   │       │       │   ├── heartBeam_metallic_1.jpg
│   │   │   │       │       │   ├── heartBeam_normal_1.png
│   │   │   │       │       │   ├── heartBeam_opacity2_1.png
│   │   │   │       │       │   ├── heartLight_M_heartLight_baseColor.png
│   │   │   │       │       │   ├── heartLight_M_heartLight_emissive.jpg
│   │   │   │       │       │   ├── heartLight_M_heartLight_metallic.jpg
│   │   │   │       │       │   ├── heartLight_M_heartLight_normal.png
│   │   │   │       │       │   ├── heartLight_M_heartLight_roughness.jpg
│   │   │   │       │       │   ├── heartLight_longer.usdc
│   │   │   │       │       │   ├── heartTurret.usdc
│   │   │   │       │       │   ├── heart_new.usdc
│   │   │   │       │       │   ├── mat_heart_Base_color_1.png
│   │   │   │       │       │   ├── mat_heart_Metallic_1.png
│   │   │   │       │       │   ├── mat_heart_Mixed_AO_1.png
│   │   │   │       │       │   ├── mat_heart_Normal_1.png
│   │   │   │       │       │   ├── mat_heart_Roughness_1.png
│   │   │   │       │       │   └── new_heart_ramp.png
│   │   │   │       │       └── HappyBeamAssets.swift
│   │   │   │       ├── Package.swift
│   │   │   │       └── README.md
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── HelloWorld
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── Packages
│   │   │   │   └── WorldAssets
│   │   │   │       ├── Package.realitycomposerpro
│   │   │   │       │   └── ProjectData
│   │   │   │       │       └── main.json
│   │   │   │       ├── Sources
│   │   │   │       │   └── WorldAssets
│   │   │   │       │       ├── WorldAssets.rkassets
│   │   │   │       │       │   ├── Moon
│   │   │   │       │       │   │   ├── 0
│   │   │   │       │       │   │   │   ├── M_moon_baseColor_1.jpg
│   │   │   │       │       │   │   │   ├── M_moon_emissive_1.jpg
│   │   │   │       │       │   │   │   ├── M_moon_metallic_1.jpg
│   │   │   │       │       │   │   │   ├── M_moon_normal_1.jpg
│   │   │   │       │       │   │   │   ├── M_moon_occlusion_1.jpg
│   │   │   │       │       │   │   │   └── M_moon_roughness_2.jpg
│   │   │   │       │       │   │   ├── M_earth_baseColor_combined.jpg
│   │   │   │       │       │   │   └── Moon.exported_compressed.usdc
│   │   │   │       │       │   ├── Pole
│   │   │   │       │       │   │   ├── 0
│   │   │   │       │       │   │   │   ├── M_arrow_baseColor_1.png
│   │   │   │       │       │   │   │   ├── M_arrow_emissive_1.jpg
│   │   │   │       │       │   │   │   ├── M_arrow_metallic_1.jpg
│   │   │   │       │       │   │   │   ├── M_arrow_normal_1.jpg
│   │   │   │       │       │   │   │   ├── M_arrow_roughness_1.jpg
│   │   │   │       │       │   │   │   └── arrow_opacity_1.png
│   │   │   │       │       │   │   └── Pole.exported_compressed.usdc
│   │   │   │       │       │   ├── Satellite
│   │   │   │       │       │   │   ├── 0
│   │   │   │       │       │   │   │   ├── M_satellite_baseColor_1.jpg
│   │   │   │       │       │   │   │   ├── M_satellite_metallic_1.jpg
│   │   │   │       │       │   │   │   ├── M_satellite_normal_1.jpg
│   │   │   │       │       │   │   │   ├── M_satellite_occlusion_1.jpg
│   │   │   │       │       │   │   │   └── M_satellite_roughness_1.jpg
│   │   │   │       │       │   │   └── Satellite.exported_compressed.usdc
│   │   │   │       │       │   ├── Sun
│   │   │   │       │       │   │   ├── 0
│   │   │   │       │       │   │   │   ├── M_sun_baseColor_1.jpg
│   │   │   │       │       │   │   │   ├── M_sun_emissive_2.jpg
│   │   │   │       │       │   │   │   ├── M_sun_metallic_1.jpg
│   │   │   │       │       │   │   │   ├── M_sun_normal_1.jpg
│   │   │   │       │       │   │   │   ├── M_sun_occlusion_1.jpg
│   │   │   │       │       │   │   │   └── M_sun_roughness_1.jpg
│   │   │   │       │       │   │   └── Sun.exported_compressed.usdc
│   │   │   │       │       │   ├── Telescope
│   │   │   │       │       │   │   ├── 0
│   │   │   │       │       │   │   │   ├── M_telescopeBase_baseColor_1.jpg
│   │   │   │       │       │   │   │   ├── M_telescopeBase_emissive_1.jpg
│   │   │   │       │       │   │   │   ├── M_telescopeBase_metallic_1.jpg
│   │   │   │       │       │   │   │   ├── M_telescopeBase_normal_1.jpg
│   │   │   │       │       │   │   │   ├── M_telescopeBase_occlusion_1.jpg
│   │   │   │       │       │   │   │   ├── M_telescopeBase_roughness_1.jpg
│   │   │   │       │       │   │   │   ├── M_telescopeReflectors_baseColor_1.png
│   │   │   │       │       │   │   │   ├── M_telescopeReflectors_emissive_1.jpg
│   │   │   │       │       │   │   │   ├── M_telescopeReflectors_metallic_1.jpg
│   │   │   │       │       │   │   │   ├── M_telescopeReflectors_normal_1.jpg
│   │   │   │       │       │   │   │   ├── M_telescopeReflectors_occlusion_1.jpg
│   │   │   │       │       │   │   │   └── M_telescopeReflectors_roughness_1.jpg
│   │   │   │       │       │   │   └── Telescope.exported_compressed.usdc
│   │   │   │       │       │   ├── Earth.usda
│   │   │   │       │       │   ├── Globe.usda
│   │   │   │       │       │   ├── Globe.usdz
│   │   │   │       │       │   ├── M_earth_baseColor.png
│   │   │   │       │       │   ├── M_earth_clouds_normal.png
│   │   │   │       │       │   ├── M_earth_emissive.jpg
│   │   │   │       │       │   ├── M_earth_normal.png
│   │   │   │       │       │   ├── M_earth_roughness.jpg
│   │   │   │       │       │   ├── Moon.usda
│   │   │   │       │       │   ├── Pole.usda
│   │   │   │       │       │   ├── Pole.usdc
│   │   │   │       │       │   ├── Satellite.usda
│   │   │   │       │       │   ├── Sun.usda
│   │   │   │       │       │   ├── Telescope.usda
│   │   │   │       │       │   ├── earthClouds_opacity.png
│   │   │   │       │       │   ├── earth_004_clouds_resized.usdc
│   │   │   │       │       │   └── earth_sphere_equirectangular.usdc
│   │   │   │       │       ├── SunPositionSystem.swift
│   │   │   │       │       └── WorldAssets.swift
│   │   │   │       ├── Package.swift
│   │   │   │       └── README.md
│   │   │   ├── World
│   │   │   │   ├── Entities
│   │   │   │   │   ├── EarthEntity+Configuration.swift
│   │   │   │   │   ├── EarthEntity.swift
│   │   │   │   │   ├── Entity+Sunlight.swift
│   │   │   │   │   ├── Entity+Trace.swift
│   │   │   │   │   ├── SatelliteEntity+Configuration.swift
│   │   │   │   │   └── SatelliteEntity.swift
│   │   │   │   ├── Globe
│   │   │   │   │   ├── Globe.swift
│   │   │   │   │   ├── GlobeControls.swift
│   │   │   │   │   ├── GlobeModule.swift
│   │   │   │   │   └── GlobeToggle.swift
│   │   │   │   ├── Model
│   │   │   │   │   ├── Module.swift
│   │   │   │   │   └── ViewModel.swift
│   │   │   │   ├── Modifiers
│   │   │   │   │   ├── DragRotationModifier.swift
│   │   │   │   │   ├── PlacementGesturesModifier.swift
│   │   │   │   │   └── TypeTextModifier.swift
│   │   │   │   ├── Modules
│   │   │   │   │   ├── ModuleCard.swift
│   │   │   │   │   ├── ModuleDetail.swift
│   │   │   │   │   ├── Modules.swift
│   │   │   │   │   └── TableOfContents.swift
│   │   │   │   ├── Orbit
│   │   │   │   │   ├── Orbit.swift
│   │   │   │   │   ├── OrbitModule.swift
│   │   │   │   │   └── OrbitToggle.swift
│   │   │   │   ├── Packages
│   │   │   │   │   └── WorldAssets
│   │   │   │   ├── Preview Content
│   │   │   │   │   └── Preview Assets.xcassets
│   │   │   │   │       └── Contents.json
│   │   │   │   ├── RealityViews
│   │   │   │   │   ├── Earth.swift
│   │   │   │   │   ├── Starfield.swift
│   │   │   │   │   └── Sun.swift
│   │   │   │   ├── Resources
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AccentColor.colorset
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   ├── Back.png
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   │   └── Front.png
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── EarthHalf.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── EarthHalf@2x.png
│   │   │   │   │   │   ├── GlobeHero.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── GlobeHero@2x.png
│   │   │   │   │   │   ├── SolarBackground.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── SolarBackground@2x.png
│   │   │   │   │   │   ├── SolarHero.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── SolarHero@2x.png
│   │   │   │   │   │   ├── Starfield.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── Starfield.jpg
│   │   │   │   │   │   ├── SunSliver.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── SunSliver@2x.png
│   │   │   │   │   │   ├── TrailGradient.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── TrailGradient.jpg
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   └── Sunlight.skybox
│   │   │   │   │       └── Sunlight.png
│   │   │   │   ├── Settings
│   │   │   │   │   ├── EarthSettings.swift
│   │   │   │   │   ├── GlobeSettings.swift
│   │   │   │   │   ├── OrbitSettings.swift
│   │   │   │   │   ├── SatelliteSettings.swift
│   │   │   │   │   ├── SettingsButton.swift
│   │   │   │   │   ├── SliderGridRow.swift
│   │   │   │   │   └── SolarSystemSettings.swift
│   │   │   │   ├── Solar System
│   │   │   │   │   ├── SolarSystem.swift
│   │   │   │   │   ├── SolarSystemControls.swift
│   │   │   │   │   ├── SolarSystemModule.swift
│   │   │   │   │   └── SolarSystemToggle.swift
│   │   │   │   ├── Systems
│   │   │   │   │   ├── RotationSystem.swift
│   │   │   │   │   └── TraceSystem.swift
│   │   │   │   ├── Info.plist
│   │   │   │   ├── InfoPlist.xcstrings
│   │   │   │   ├── Localizable.xcstrings
│   │   │   │   └── WorldApp.swift
│   │   │   ├── World.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── World.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── ObjectPlacementExample
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── ObjectPlacement
│   │   │   │   ├── 3D Models
│   │   │   │   │   ├── Box.usdz
│   │   │   │   │   ├── Cone.usdz
│   │   │   │   │   ├── Cube.usdz
│   │   │   │   │   └── Cylinder.usdz
│   │   │   │   ├── App
│   │   │   │   │   ├── AppState.swift
│   │   │   │   │   ├── DragState.swift
│   │   │   │   │   ├── PlaceableObject.swift
│   │   │   │   │   ├── PlacementManager.swift
│   │   │   │   │   └── PlacementState.swift
│   │   │   │   ├── Utilities
│   │   │   │   │   ├── GeometryUtilities.swift
│   │   │   │   │   ├── ModelLoader.swift
│   │   │   │   │   ├── PersistenceManager.swift
│   │   │   │   │   ├── PlaneAnchorHandler.swift
│   │   │   │   │   └── PlaneProjector.swift
│   │   │   │   ├── Views
│   │   │   │   │   ├── DeleteButton.swift
│   │   │   │   │   ├── HomeView.swift
│   │   │   │   │   ├── InfoLabel.swift
│   │   │   │   │   ├── ObjectPlacementMenuView.swift
│   │   │   │   │   ├── ObjectPlacementRealityView.swift
│   │   │   │   │   ├── ObjectSelectionView.swift
│   │   │   │   │   ├── PlacementTooltip.swift
│   │   │   │   │   └── TooltipView.swift
│   │   │   │   ├── Info.plist
│   │   │   │   └── ObjectPlacementApp.swift
│   │   │   ├── ObjectPlacement.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       ├── xcschemes
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── ObjectPlacement.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── PlayingSpatialAudioInVisionOS
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── SpatialAudio
│   │   │   │   ├── App
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── EntryPoint.swift
│   │   │   │   │   └── Info.plist
│   │   │   │   ├── Resources
│   │   │   │   │   └── FunkySynth.m4a
│   │   │   │   ├── Views
│   │   │   │   │   ├── DecibelSlider.swift
│   │   │   │   │   └── SpatialAudioView.swift
│   │   │   │   └── Visualizer
│   │   │   │       └── AxisVisualizer.swift
│   │   │   ├── SpatialAudio.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── SceneReconstructionExample
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── SceneReconstructionExample
│   │   │   │   ├── ContentView.swift
│   │   │   │   ├── CubeMeshInteraction.swift
│   │   │   │   ├── EntityModel.swift
│   │   │   │   ├── Extensions.swift
│   │   │   │   ├── Info.plist
│   │   │   │   └── SceneReconstructionExampleApp.swift
│   │   │   ├── SceneReconstructionExample.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       ├── xcschemes
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── SwiftSplash
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── Packages
│   │   │   │   └── SwiftSplashTrackPieces
│   │   │   │       ├── Package.realitycomposerpro
│   │   │   │       │   ├── ProjectData
│   │   │   │       │   │   └── main.json
│   │   │   │       │   └── WorkspaceData
│   │   │   │       │       ├── SceneMetadataList.json
│   │   │   │       │       ├── Settings.rcprojectdata
│   │   │   │       │       └── amandaestrada.rcuserdata
│   │   │   │       ├── Sources
│   │   │   │       │   └── SwiftSplashTrackPieces
│   │   │   │       │       ├── Components
│   │   │   │       │       │   ├── Connectable.swift
│   │   │   │       │       │   ├── ConnectableStateComponent.swift
│   │   │   │       │       │   └── MarkerComponents.swift
│   │   │   │       │       ├── Extensions
│   │   │   │       │       │   ├── Entity+Utilities.swift
│   │   │   │       │       │   ├── Float+Utilities.swift
│   │   │   │       │       │   └── SIMD+Utilities.swift
│   │   │   │       │       ├── SwiftSplashTrackPieces.rkassets
│   │   │   │       │       │   ├── Fish
│   │   │   │       │       │   │   ├── Textures
│   │   │   │       │       │   │   │   ├── mat_fishAccessories_BaseColor.png
│   │   │   │       │       │   │   │   ├── mat_fishAccessories_Normal.png
│   │   │   │       │       │   │   │   ├── mat_fishAccessories_OcclusionRoughnessMetallic.png
│   │   │   │       │       │   │   │   ├── mat_fishAccessories_Roughness.png
│   │   │   │       │       │   │   │   ├── mat_fishBody_BaseColor.png
│   │   │   │       │       │   │   │   ├── mat_fishBody_Normal.png
│   │   │   │       │       │   │   │   ├── mat_fishBody_OcclusionRoughnessMetallic.png
│   │   │   │       │       │   │   │   ├── mat_fishBody_Roughness.png
│   │   │   │       │       │   │   │   ├── mat_fishEyes_BaseColor.png
│   │   │   │       │       │   │   │   ├── mat_fishEyes_Normal.png
│   │   │   │       │       │   │   │   ├── mat_fishEyes_OcclusionRoughnessMetallic.png
│   │   │   │       │       │   │   │   ├── mat_fishGlass_BaseColor.png
│   │   │   │       │       │   │   │   ├── mat_fishGlass_Normal.png
│   │   │   │       │       │   │   │   └── mat_fishGlass_OcclusionRoughnessMetallic.png
│   │   │   │       │       │   │   ├── animations
│   │   │   │       │       │   │   │   └── adventureFish_swim_slide01_anim.usdz
│   │   │   │       │       │   │   ├── adventureFish_idle_001_anim.usdz
│   │   │   │       │       │   │   └── adventureFish_swim_001_anim.usdz
│   │   │   │       │       │   ├── Goal
│   │   │   │       │       │   │   ├── Fish
│   │   │   │       │       │   │   │   ├── adventureFish_end_glass_idle_animation.usdz
│   │   │   │       │       │   │   │   ├── adventureFish_end_glass_ride_animation.usdz
│   │   │   │       │       │   │   │   ├── adventureFish_end_noGlass_idle_animation.usdz
│   │   │   │       │       │   │   │   └── adventureFish_end_noGlass_ride_animation.usdz
│   │   │   │       │       │   │   ├── end.usdz
│   │   │   │       │       │   │   ├── end_flag_glow.usd
│   │   │   │       │       │   │   ├── end_glow.usd
│   │   │   │       │       │   │   ├── end_water.usd
│   │   │   │       │       │   │   ├── flag_idle_animation.usdz
│   │   │   │       │       │   │   ├── flag_still_geo.usdz
│   │   │   │       │       │   │   ├── slideEnd_bottom.usdz
│   │   │   │       │       │   │   ├── slideEnd_top.usd
│   │   │   │       │       │   │   ├── slideEnd_top_glow.usd
│   │   │   │       │       │   │   ├── slide_end_water.usdz
│   │   │   │       │       │   │   └── waterFallSplash.usdz
│   │   │   │       │       │   ├── ParticleEmitterPresetTextures
│   │   │   │       │       │   │   ├── dustsheet.exr
│   │   │   │       │       │   │   ├── flare.exr
│   │   │   │       │       │   │   ├── flaresheet.exr
│   │   │   │       │       │   │   ├── halfRadial.png
│   │   │   │       │       │   │   ├── halfRadial1.png
│   │   │   │       │       │   │   ├── rain.png
│   │   │   │       │       │   │   ├── splashSpriteSheet.png
│   │   │   │       │       │   │   ├── testSplash.png
│   │   │   │       │       │   │   ├── twinkle.exr
│   │   │   │       │       │   │   └── waterDrop.png
│   │   │   │       │       │   ├── Slide_01
│   │   │   │       │       │   │   ├── Fish
│   │   │   │       │       │   │   │   ├── adventureFish_slide01_glass_ride_animation.usdz
│   │   │   │       │       │   │   │   └── adventureFish_slide01_noGlass_ride_animation.usdz
│   │   │   │       │       │   │   ├── slide01_bottom.usdz
│   │   │   │       │       │   │   ├── slide01_bottom_glow.usd
│   │   │   │       │       │   │   ├── slide01_top.usdz
│   │   │   │       │       │   │   ├── slide01_top_glow.usdz
│   │   │   │       │       │   │   ├── slide01_water.usdz
│   │   │   │       │       │   │   └── slide_01.usdz
│   │   │   │       │       │   ├── Slide_02
│   │   │   │       │       │   │   ├── Fish
│   │   │   │       │       │   │   │   ├── adventureFish_slide02_glass_ride_animation.usdz
│   │   │   │       │       │   │   │   └── adventureFish_slide02_noGlass_ride_animation.usdz
│   │   │   │       │       │   │   ├── slide02_bottom.usdz
│   │   │   │       │       │   │   ├── slide02_bottom_glow.usdz
│   │   │   │       │       │   │   ├── slide02_top.usdz
│   │   │   │       │       │   │   ├── slide02_top_glow.usd
│   │   │   │       │       │   │   └── slide02_water.usdz
│   │   │   │       │       │   ├── Slide_03
│   │   │   │       │       │   │   ├── Fish
│   │   │   │       │       │   │   │   ├── adventureFish_slide03_glass_ride_animation.usdz
│   │   │   │       │       │   │   │   └── adventureFish_slide03_noGlass_ride_animation.usdz
│   │   │   │       │       │   │   ├── slide03_bottom.usdz
│   │   │   │       │       │   │   ├── slide03_bottom_glow.usdz
│   │   │   │       │       │   │   ├── slide03_top.usdz
│   │   │   │       │       │   │   ├── slide03_top_glow.usdz
│   │   │   │       │       │   │   └── slide03_water.usdz
│   │   │   │       │       │   ├── Slide_04
│   │   │   │       │       │   │   ├── adventureFish_slide04_glass_ride_animation.usdz
│   │   │   │       │       │   │   ├── adventureFish_slide04_noGlass_ride_animation.usdz
│   │   │   │       │       │   │   ├── adventureFish_slide04_ride_animation.usdz
│   │   │   │       │       │   │   ├── slide04_bottom.usdz
│   │   │   │       │       │   │   ├── slide04_bottom_glow.usdz
│   │   │   │       │       │   │   ├── slide04_top.usdz
│   │   │   │       │       │   │   ├── slide04_top_glow.usdz
│   │   │   │       │       │   │   └── slide04_water.usdz
│   │   │   │       │       │   ├── Slide_05
│   │   │   │       │       │   │   ├── Fish
│   │   │   │       │       │   │   │   ├── adventureFish_slide05_glass_ride_animation.usdz
│   │   │   │       │       │   │   │   └── adventureFish_slide05_noGlass_ride_animation.usdz
│   │   │   │       │       │   │   ├── slide05_bottom.usdz
│   │   │   │       │       │   │   ├── slide05_bottom_glow.usdz
│   │   │   │       │       │   │   ├── slide05_top.usdz
│   │   │   │       │       │   │   ├── slide05_top_glow.usdz
│   │   │   │       │       │   │   └── slide05_water.usdz
│   │   │   │       │       │   ├── Start
│   │   │   │       │       │   │   ├── adventureFish_start_glass_idle_animation.usdz
│   │   │   │       │       │   │   ├── adventureFish_start_glass_ride_animation.usdz
│   │   │   │       │       │   │   ├── adventureFish_start_noGlass_idle_animation.usdz
│   │   │   │       │       │   │   ├── adventureFish_start_noGlass_ride_animation.usdz
│   │   │   │       │       │   │   ├── slideStart_bottom.usd
│   │   │   │       │       │   │   ├── slideStart_water.usdz
│   │   │   │       │       │   │   ├── start_glass.usd
│   │   │   │       │       │   │   ├── start_glow.usdz
│   │   │   │       │       │   │   ├── start_ride_animation.usdz
│   │   │   │       │       │   │   └── waterDrain_ride_animation.usdz
│   │   │   │       │       │   ├── Textures
│   │   │   │       │       │   │   ├── Metal
│   │   │   │       │       │   │   │   ├── mat_end_BaseColor_metal.png
│   │   │   │       │       │   │   │   ├── mat_end_Normal_metal.png
│   │   │   │       │       │   │   │   ├── mat_end_OcclusionRoughnessMetallic_metal.png
│   │   │   │       │       │   │   │   ├── mat_end_OcclusionRoughnessMetallic_plastic.png
│   │   │   │       │       │   │   │   ├── mat_slideTop_BaseColor_metal.png
│   │   │   │       │       │   │   │   ├── mat_slideTop_Emissive_metal.png
│   │   │   │       │       │   │   │   ├── mat_slideTop_Normal_metal.png
│   │   │   │       │       │   │   │   ├── mat_slideTop_OcclusionRoughnessMetallic_metal.png
│   │   │   │       │       │   │   │   ├── mat_slide_BaseColor_metal.png
│   │   │   │       │       │   │   │   ├── mat_slide_Normal_metal.png
│   │   │   │       │       │   │   │   ├── mat_slide_OcclusionRoughnessMetallic_metal.png
│   │   │   │       │       │   │   │   ├── mat_start_BaseColor_metal.png
│   │   │   │       │       │   │   │   ├── mat_start_Normal_metal.png
│   │   │   │       │       │   │   │   ├── mat_start_OcclusionRoughnessMetallic_metal.png
│   │   │   │       │       │   │   │   └── waterRidePieces_mat_slideTop_Opacity.png
│   │   │   │       │       │   │   ├── Plastic
│   │   │   │       │       │   │   │   ├── mat_end_BaseColor_plastic.png
│   │   │   │       │       │   │   │   ├── mat_end_Normal_plastic.png
│   │   │   │       │       │   │   │   ├── mat_end_OcclusionRoughnessMetallic_plastic.png
│   │   │   │       │       │   │   │   ├── mat_slide_BaseColor_plastic.png
│   │   │   │       │       │   │   │   ├── mat_slide_Normal_plastic.png
│   │   │   │       │       │   │   │   ├── mat_slide_OcclusionRoughnessMetallic_plastic.png
│   │   │   │       │       │   │   │   ├── mat_start_BaseColor_plastic.png
│   │   │   │       │       │   │   │   ├── mat_start_Normal_plastic.png
│   │   │   │       │       │   │   │   └── mat_start_OcclusionRoughnessMetallic_plastic.png
│   │   │   │       │       │   │   ├── Universal
│   │   │   │       │       │   │   │   ├── masks
│   │   │   │       │       │   │   │   │   ├── gradientMask.png
│   │   │   │       │       │   │   │   │   ├── water_ramp.png
│   │   │   │       │       │   │   │   │   └── water_ramp_2.png
│   │   │   │       │       │   │   │   ├── water
│   │   │   │       │       │   │   │   │   ├── Noise.PNG
│   │   │   │       │       │   │   │   │   ├── cloudsNoise .png
│   │   │   │       │       │   │   │   │   ├── endWater.png
│   │   │   │       │       │   │   │   │   ├── end_water_normal.png
│   │   │   │       │       │   │   │   │   ├── flowmap7.png
│   │   │   │       │       │   │   │   │   ├── flowmap8.png
│   │   │   │       │       │   │   │   │   ├── movingWater_AO.png
│   │   │   │       │       │   │   │   │   ├── movingWater_BC.png
│   │   │   │       │       │   │   │   │   ├── movingWater_H.png
│   │   │   │       │       │   │   │   │   ├── movingWater_N.png
│   │   │   │       │       │   │   │   │   ├── stagnantWater_AO.png
│   │   │   │       │       │   │   │   │   ├── stagnantWater_BC.png
│   │   │   │       │       │   │   │   │   ├── stagnantWater_H.png
│   │   │   │       │       │   │   │   │   ├── stagnantWater_N.png
│   │   │   │       │       │   │   │   │   ├── waterFallMask.png
│   │   │   │       │       │   │   │   │   └── waterFallMask2.png
│   │   │   │       │       │   │   │   ├── M_aquariumGlass_emissive.jpg
│   │   │   │       │       │   │   │   ├── mat_aquariumGlass_BaseColor.png
│   │   │   │       │       │   │   │   ├── mat_aquariumGlass_Emissive.png
│   │   │   │       │       │   │   │   ├── mat_aquariumGlass_Normal.png
│   │   │   │       │       │   │   │   ├── mat_aquariumGlass_OcclusionRoughnessMetallic.png
│   │   │   │       │       │   │   │   ├── mat_aquariumGlass_Opacity.png
│   │   │   │       │       │   │   │   ├── mat_lightsRim_BaseColor.png
│   │   │   │       │       │   │   │   ├── mat_lightsRim_Normal.png
│   │   │   │       │       │   │   │   ├── mat_lightsRim_OcclusionRoughnessMetallic.png
│   │   │   │       │       │   │   │   ├── mat_rainbowLights_BaseColor.png
│   │   │   │       │       │   │   │   ├── mat_rainbowLights_Normal.png
│   │   │   │       │       │   │   │   ├── mat_rainbowLights_OcclusionRoughnessMetallic.png
│   │   │   │       │       │   │   │   ├── mat_rainbowLights_emmissive.png
│   │   │   │       │       │   │   │   ├── mat_slideLights_BaseColor.png
│   │   │   │       │       │   │   │   ├── mat_slideLights_Normal.png
│   │   │   │       │       │   │   │   ├── mat_slideLights_OcclusionRoughnessMetallic.png
│   │   │   │       │       │   │   │   └── noise.png
│   │   │   │       │       │   │   └── Wood
│   │   │   │       │       │   │       ├── mat_end_BaseColor_wood.png
│   │   │   │       │       │   │       ├── mat_end_Normal_wood.png
│   │   │   │       │       │   │       ├── mat_end_OcclusionRoughnessMetallic_wood.png
│   │   │   │       │       │   │       ├── mat_slide_BaseColor_wood.png
│   │   │   │       │       │   │       ├── mat_slide_Normal_wood.png
│   │   │   │       │       │   │       ├── mat_slide_OcclusionRoughnessMetallic_wood.png
│   │   │   │       │       │   │       ├── mat_start_BaseColor_wood.png
│   │   │   │       │       │   │       ├── mat_start_Normal_wood.png
│   │   │   │       │       │   │       └── mat_start_OcclusionRoughnessMetallic_wood.png
│   │   │   │       │       │   ├── waterTest
│   │   │   │       │       │   │   ├── slide01_water.usd
│   │   │   │       │       │   │   └── slide02_water.usd
│   │   │   │       │       │   ├── EndParticles.usda
│   │   │   │       │       │   ├── EndPiece.usda
│   │   │   │       │       │   ├── FishMaterials.usda
│   │   │   │       │       │   ├── M_Glow.usda
│   │   │   │       │       │   ├── M_LightsRim.usda
│   │   │   │       │       │   ├── M_MovingWater.usda
│   │   │   │       │       │   ├── M_RainbowLights.usda
│   │   │   │       │       │   ├── M_SlideBottom.usda
│   │   │   │       │       │   ├── M_SlideLights.usda
│   │   │   │       │       │   ├── M_SlideTop.usda
│   │   │   │       │       │   ├── M_SolidSpheres.usda
│   │   │   │       │       │   ├── M_StagnantWater.usda
│   │   │   │       │       │   ├── M_WaterFall.usda
│   │   │   │       │       │   ├── M_endWater
│   │   │   │       │       │   ├── M_endWater.usda
│   │   │   │       │       │   ├── M_solidSpheres_emmissive.png
│   │   │   │       │       │   ├── Slide01.usda
│   │   │   │       │       │   ├── Slide02.usda
│   │   │   │       │       │   ├── Slide03.usda
│   │   │   │       │       │   ├── Slide04.usda
│   │   │   │       │       │   ├── Slide05.usda
│   │   │   │       │       │   ├── StartPiece.usda
│   │   │   │       │       │   ├── SwiftSplashTrackPieces.usda
│   │   │   │       │       │   ├── Untitled.usda
│   │   │   │       │       │   ├── WaterRideMaterials.usda
│   │   │   │       │       │   ├── distortion.usda
│   │   │   │       │       │   ├── glow_mask.png
│   │   │   │       │       │   ├── solidSpheres.usda
│   │   │   │       │       │   ├── solidSpheres.usdz
│   │   │   │       │       │   └── sphere_opacity.png
│   │   │   │       │       └── SwiftSplashTrackPieces.swift
│   │   │   │       ├── build
│   │   │   │       │   ├── EagerLinkingTBDs
│   │   │   │       │   │   └── Release-xros
│   │   │   │       │   ├── Release-xros
│   │   │   │       │   │   ├── PackageFrameworks
│   │   │   │       │   │   └── SwiftSplashTrackPieces_SwiftSplashTrackPieces.bundle
│   │   │   │       │   └── SwiftSplashTrackPieces.build
│   │   │   │       │       └── Release-xros
│   │   │   │       │           └── SwiftSplashTrackPieces_SwiftSplashTrackPieces.build
│   │   │   │       │               ├── DerivedSources
│   │   │   │       │               │   └── RealityAssetsGenerated
│   │   │   │       │               │       ├── CustomComponentUSDInitializers.usda
│   │   │   │       │               │       └── ModuleWithDependencies.json
│   │   │   │       │               ├── 7edbc1cc5cc2d7d899440c5ab7769731.sb
│   │   │   │       │               └── c9838f0f8c26148c3a159ab43e96009e.sb
│   │   │   │       ├── Package.swift
│   │   │   │       └── README.md
│   │   │   ├── SwiftSplash
│   │   │   │   ├── Assets
│   │   │   │   │   ├── deletePiece.wav
│   │   │   │   │   ├── endRide.wav
│   │   │   │   │   ├── fishSound_longLoudHappy.wav
│   │   │   │   │   ├── fishSound_mediumHappy.wav
│   │   │   │   │   ├── fishSound_quietHappy.wav
│   │   │   │   │   ├── pickUp.wav
│   │   │   │   │   ├── placePiece.wav
│   │   │   │   │   ├── startRide.wav
│   │   │   │   │   ├── swiftSplash_BuildMode.wav
│   │   │   │   │   ├── swiftSplash_Menu.wav
│   │   │   │   │   ├── swiftSplash_RideMode.m4a
│   │   │   │   │   └── waterFlowing.wav
│   │   │   │   ├── Assets.xcassets
│   │   │   │   │   ├── AccentColor.colorset
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   └── SPIcon_bottom.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   └── SPIcon_middle.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   └── SPIcon_top.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── goal_metal.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── goal_metal.png
│   │   │   │   │   ├── goal_plastic.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── goal_plastic.png
│   │   │   │   │   ├── goal_wood.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── goal_wood.png
│   │   │   │   │   ├── metalPreview.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── metalPreview@2x.png
│   │   │   │   │   ├── plasticPreview.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── plasticPreview@2x.png
│   │   │   │   │   ├── slide_01_metal.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_01_metal.png
│   │   │   │   │   ├── slide_01_plastic.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_01_plastic.png
│   │   │   │   │   ├── slide_01_wood.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_01_wood.png
│   │   │   │   │   ├── slide_02_metal.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_02_metal.png
│   │   │   │   │   ├── slide_02_plastic.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_02_plastic.png
│   │   │   │   │   ├── slide_02_wood.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_02_wood.png
│   │   │   │   │   ├── slide_03_metal.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_03_metal.png
│   │   │   │   │   ├── slide_03_plastic.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_03_plastic.png
│   │   │   │   │   ├── slide_03_wood.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_03_wood.png
│   │   │   │   │   ├── slide_04_metal.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_04_metal.png
│   │   │   │   │   ├── slide_04_plastic.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_04_plastic.png
│   │   │   │   │   ├── slide_04_wood.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_04_wood.png
│   │   │   │   │   ├── slide_05_metal.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_05_metal.png
│   │   │   │   │   ├── slide_05_plastic.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_05_plastic.png
│   │   │   │   │   ├── slide_05_wood.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_05_wood.png
│   │   │   │   │   ├── swiftSplashHero.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── swiftSplashHero@2x.png
│   │   │   │   │   ├── woodPreview.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── woodPreview@2x.png
│   │   │   │   │   └── Contents.json
│   │   │   │   ├── Data & State
│   │   │   │   │   ├── AppConfig.swift
│   │   │   │   │   ├── AppPhase.swift
│   │   │   │   │   ├── AppState+Phases.swift
│   │   │   │   │   ├── AppState+PieceLoading.swift
│   │   │   │   │   ├── AppState+PieceManagement.swift
│   │   │   │   │   ├── AppState+PieceSelection.swift
│   │   │   │   │   ├── AppState+RideRunning.swift
│   │   │   │   │   ├── AppState+TrackUpdates.swift
│   │   │   │   │   ├── AppState+Transparency.swift
│   │   │   │   │   ├── AppState.swift
│   │   │   │   │   ├── Piece.swift
│   │   │   │   │   └── SoundEffects.swift
│   │   │   │   ├── Extensions
│   │   │   │   │   ├── Date+Logging.swift
│   │   │   │   │   └── Entity+SwiftSplash.swift
│   │   │   │   ├── Preview Content
│   │   │   │   │   └── Preview Assets.xcassets
│   │   │   │   │       └── Contents.json
│   │   │   │   ├── Views
│   │   │   │   │   ├── Sources
│   │   │   │   │   │   └── Views
│   │   │   │   │   │       └── Views.rkassets
│   │   │   │   │   │           └── Scene.usda
│   │   │   │   │   ├── ContentToolbar.swift
│   │   │   │   │   ├── ContentView.swift
│   │   │   │   │   ├── EditTrackPieceView.swift
│   │   │   │   │   ├── ImageButton.swift
│   │   │   │   │   ├── PieceShelfTrackButtonsView.swift
│   │   │   │   │   ├── PieceShelfView.swift
│   │   │   │   │   ├── PlaceStartPieceView.swift
│   │   │   │   │   ├── RideControlView.swift
│   │   │   │   │   ├── SplashScreenView.swift
│   │   │   │   │   ├── TrackBuildingView+Drag.swift
│   │   │   │   │   ├── TrackBuildingView+Rotation.swift
│   │   │   │   │   ├── TrackBuildingView+Snapping.swift
│   │   │   │   │   └── TrackBuildingView.swift
│   │   │   │   ├── de.lproj
│   │   │   │   ├── fr.lproj
│   │   │   │   ├── ja.lproj
│   │   │   │   ├── ko.lproj
│   │   │   │   ├── zh_CN.lproj
│   │   │   │   ├── InfoPlist.xcstrings
│   │   │   │   ├── Localizable.xcstrings
│   │   │   │   └── SwiftSplashApp.swift
│   │   │   ├── SwiftSplash.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── SwiftSplash.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── TrackingAndVisualizingHandMovement
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── RealityKit-HandTracking
│   │   │   │   ├── App
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── HandTracking.swift
│   │   │   │   │   └── Info.plist
│   │   │   │   ├── Entities
│   │   │   │   │   ├── Bone.swift
│   │   │   │   │   ├── Finger.swift
│   │   │   │   │   └── Hand.swift
│   │   │   │   ├── Systems
│   │   │   │   │   └── ClosureComponent.swift
│   │   │   │   └── Views
│   │   │   │       ├── HandTrackingView.swift
│   │   │   │       └── MainView.swift
│   │   │   ├── RealityKit-HandTracking.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── adding-a-depth-effect-to-text-in-visionos
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── DepthText
│   │   │   │   ├── App
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── EntryPoint.swift
│   │   │   │   │   └── Info.plist
│   │   │   │   └── Views
│   │   │   │       ├── DepthTextView.swift
│   │   │   │       └── MainView.swift
│   │   │   ├── DepthText.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── bot-anist
│   │   │   ├── BOT-anist
│   │   │   │   ├── Assets.xcassets
│   │   │   │   │   ├── AccentColor.colorset
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── HeroRobot.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── HeroRobot@2x.png
│   │   │   │   │   ├── VisionOSAppIcon.solidimagestack
│   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   ├── Back.png
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   └── Front.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── backpack1.imageset
│   │   │   │   │   │   ├── BP1 (2) 1.png
│   │   │   │   │   │   ├── BP1 (2).png
│   │   │   │   │   │   ├── BP1_dark (2).png
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── backpack2.imageset
│   │   │   │   │   │   ├── BP2 (2) 1.png
│   │   │   │   │   │   ├── BP2 (2).png
│   │   │   │   │   │   ├── BP2_dark (2).png
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── backpack3.imageset
│   │   │   │   │   │   ├── BP3 (2) 1.png
│   │   │   │   │   │   ├── BP3 (2).png
│   │   │   │   │   │   ├── BP3_dark (2).png
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── body1.imageset
│   │   │   │   │   │   ├── B1 1.png
│   │   │   │   │   │   ├── B1.png
│   │   │   │   │   │   ├── B1_dark.png
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── body2.imageset
│   │   │   │   │   │   ├── B2 1.png
│   │   │   │   │   │   ├── B2.png
│   │   │   │   │   │   ├── B2_dark.png
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── body3.imageset
│   │   │   │   │   │   ├── B3 1.png
│   │   │   │   │   │   ├── B3.png
│   │   │   │   │   │   ├── B3_dark.png
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── circle.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   ├── oval 1.png
│   │   │   │   │   │   ├── oval.png
│   │   │   │   │   │   └── oval_dark.png
│   │   │   │   │   ├── head1.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   ├── H1 (1) 1.png
│   │   │   │   │   │   ├── H1 (1).png
│   │   │   │   │   │   └── H1_dark (1).png
│   │   │   │   │   ├── head2.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   ├── H2 (1) 1.png
│   │   │   │   │   │   ├── H2 (1).png
│   │   │   │   │   │   └── H2_dark (1).png
│   │   │   │   │   ├── head3.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   ├── H3 (1) 1.png
│   │   │   │   │   │   ├── H3 (1).png
│   │   │   │   │   │   └── H3_dark (1).png
│   │   │   │   │   ├── heart.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   ├── hearts 1.png
│   │   │   │   │   │   ├── hearts.png
│   │   │   │   │   │   └── hearts_dark.png
│   │   │   │   │   ├── iOSAppIcon.appiconset
│   │   │   │   │   │   ├── AppIcon.png
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   ├── DarkAppIcon.png
│   │   │   │   │   │   └── TintableAppIcon.png
│   │   │   │   │   ├── macOSAppIcon.appiconset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   ├── icon_128x128.png
│   │   │   │   │   │   ├── icon_128x128@2x.png
│   │   │   │   │   │   ├── icon_16x16.png
│   │   │   │   │   │   ├── icon_16x16@2x.png
│   │   │   │   │   │   ├── icon_256x256.png
│   │   │   │   │   │   ├── icon_256x256@2x.png
│   │   │   │   │   │   ├── icon_32x32.png
│   │   │   │   │   │   ├── icon_32x32@2x.png
│   │   │   │   │   │   ├── icon_512x512.png
│   │   │   │   │   │   └── icon_512x512@2x.png
│   │   │   │   │   ├── mesh.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── mesh.png
│   │   │   │   │   ├── metal.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── metal.png
│   │   │   │   │   ├── plastic.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── plastic.png
│   │   │   │   │   ├── rainbow.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── rainbow.png
│   │   │   │   │   ├── square.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   ├── digitalSquares (1) 1.png
│   │   │   │   │   │   ├── digitalSquares (1).png
│   │   │   │   │   │   └── digitalSquares.png
│   │   │   │   │   └── Contents.json
│   │   │   │   ├── Components
│   │   │   │   │   └── JointPinComponent.swift
│   │   │   │   ├── Extensions
│   │   │   │   │   ├── CaseIterableExtensions.swift
│   │   │   │   │   ├── ColorExtensions.swift
│   │   │   │   │   ├── EntityExtensions.swift
│   │   │   │   │   ├── Preview+AppStateEnvironment.swift
│   │   │   │   │   ├── RealityView+KeyboardControls.swift
│   │   │   │   │   ├── RealityView+TouchControls.swift
│   │   │   │   │   └── StringExtensions.swift
│   │   │   │   ├── Preview Content
│   │   │   │   │   └── Preview Assets.xcassets
│   │   │   │   │       └── Contents.json
│   │   │   │   ├── Robot
│   │   │   │   │   ├── AnimationStateMachine.swift
│   │   │   │   │   ├── RobotCharacter+Movement.swift
│   │   │   │   │   ├── RobotCharacter.swift
│   │   │   │   │   ├── RobotData.swift
│   │   │   │   │   ├── RobotProvider+Loading.swift
│   │   │   │   │   └── RobotProvider.swift
│   │   │   │   ├── Skybox
│   │   │   │   │   └── autumn_field_puresky_1k.png
│   │   │   │   ├── Systems
│   │   │   │   │   └── JointPinSystem.swift
│   │   │   │   ├── Views
│   │   │   │   │   ├── ContentView.swift
│   │   │   │   │   ├── ExplorationView.swift
│   │   │   │   │   ├── OrnamentView.swift
│   │   │   │   │   ├── RobotCustomizationView.swift
│   │   │   │   │   ├── RobotView.swift
│   │   │   │   │   ├── SelectorViews.swift
│   │   │   │   │   └── StartScreenView.swift
│   │   │   │   ├── AppState+Exploration.swift
│   │   │   │   ├── AppState.swift
│   │   │   │   ├── BOT-anist-InfoPlist.xcstrings
│   │   │   │   ├── BOT-anist.entitlements
│   │   │   │   ├── BOTanistApp.swift
│   │   │   │   ├── Localizable.xcstrings
│   │   │   │   └── PlantAnimationProvider.swift
│   │   │   ├── BOT-anist.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── BOTanist.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── Packages
│   │   │   │   └── BOTanistAssets
│   │   │   │       ├── Package.realitycomposerpro
│   │   │   │       │   ├── ProjectData
│   │   │   │       │   │   └── main.json
│   │   │   │       │   └── WorkspaceData
│   │   │   │       │       └── Settings.rcprojectdata
│   │   │   │       ├── Sources
│   │   │   │       │   └── BOTanistAssets
│   │   │   │       │       ├── BOTanistAssets.rkassets
│   │   │   │       │       │   ├── Assets
│   │   │   │       │       │   │   ├── Robot
│   │   │   │       │       │   │   │   ├── animations
│   │   │   │       │       │   │   │   │   ├── body1
│   │   │   │       │       │   │   │   │   │   ├── body1_celebrate_anim.usd
│   │   │   │       │       │   │   │   │   │   ├── body1_idle_anim.usd
│   │   │   │       │       │   │   │   │   │   ├── body1_walkEnd_anim.usd
│   │   │   │       │       │   │   │   │   │   ├── body1_walkLoop_anim.usd
│   │   │   │       │       │   │   │   │   │   └── body1_wave_anim.usd
│   │   │   │       │       │   │   │   │   ├── body2
│   │   │   │       │       │   │   │   │   │   ├── body2_celebrate_anim.usd
│   │   │   │       │       │   │   │   │   │   ├── body2_idle_anim.usd
│   │   │   │       │       │   │   │   │   │   ├── body2_walkEnd_anim.usd
│   │   │   │       │       │   │   │   │   │   ├── body2_walkLoop_anim.usd
│   │   │   │       │       │   │   │   │   │   └── body2_wave_anim.usd
│   │   │   │       │       │   │   │   │   └── body3
│   │   │   │       │       │   │   │   │       ├── body3_celebrate_anim.usd
│   │   │   │       │       │   │   │   │       ├── body3_idle_anim.usd
│   │   │   │       │       │   │   │   │       ├── body3_walkEnd_anim.usd
│   │   │   │       │       │   │   │   │       ├── body3_walkLoop_anim.usd
│   │   │   │       │       │   │   │   │       └── body3_wave_anim.usd
│   │   │   │       │       │   │   │   ├── mesh
│   │   │   │       │       │   │   │   │   ├── backpack1.usdz
│   │   │   │       │       │   │   │   │   ├── backpack2.usdz
│   │   │   │       │       │   │   │   │   ├── backpack3.usdz
│   │   │   │       │       │   │   │   │   ├── body1.usdz
│   │   │   │       │       │   │   │   │   ├── body2.usdz
│   │   │   │       │       │   │   │   │   ├── body3.usdz
│   │   │   │       │       │   │   │   │   ├── head1.usdz
│   │   │   │       │       │   │   │   │   ├── head2.usdz
│   │   │   │       │       │   │   │   │   └── head3.usdz
│   │   │   │       │       │   │   │   ├── sounds
│   │   │   │       │       │   │   │   │   └── scratch
│   │   │   │       │       │   │   │   │       ├── body1_walk_step1.mp3
│   │   │   │       │       │   │   │   │       └── body1_walk_step2.mp3
│   │   │   │       │       │   │   │   └── textures
│   │   │   │       │       │   │   │       ├── eyes
│   │   │   │       │       │   │   │       │   ├── eyes1_blink_anim.jpg
│   │   │   │       │       │   │   │       │   ├── eyes2_blink_anim.jpg
│   │   │   │       │       │   │   │       │   └── eyes3_blink_anim.jpg
│   │   │   │       │       │   │   │       ├── lights
│   │   │   │       │       │   │   │       │   ├── PB.jpg
│   │   │   │       │       │   │   │       │   ├── PB_2.jpg
│   │   │   │       │       │   │   │       │   ├── PB_3.jpg
│   │   │   │       │       │   │   │       │   ├── RB.jpg
│   │   │   │       │       │   │   │       │   ├── RB_2.jpg
│   │   │   │       │       │   │   │       │   ├── RB_3.jpg
│   │   │   │       │       │   │   │       │   └── stripes_Mask.jpg
│   │   │   │       │       │   │   │       ├── mesh
│   │   │   │       │       │   │   │       │   ├── backpack1
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_mesh_black.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_mesh_grey.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_mesh_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_mesh_yellow.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Metalness_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Normal_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Opacity_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_backpack1_Roughness_mesh_.jpg
│   │   │   │       │       │   │   │       │   ├── backpack2
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_mesh_black.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_mesh_grey.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_mesh_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_mesh_yellow.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Metalness_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Normal_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Opacity_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_backpack2_Roughness_mesh_.jpg
│   │   │   │       │       │   │   │       │   ├── backpack3
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_mesh_black.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_mesh_grey.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_mesh_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_mesh_yellow.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Metalness_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Normal_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Opacity_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_backpack3_Roughness_mesh_.jpg
│   │   │   │       │       │   │   │       │   ├── body1
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_mesh_black.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_mesh_grey.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_mesh_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_mesh_yellow.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_Normal_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_body1_Roughness_mesh_.jpg
│   │   │   │       │       │   │   │       │   ├── body2
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_mesh_black.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_mesh_grey.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_mesh_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_mesh_yellow.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_Normal_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_body2_Roughness_mesh_.jpg
│   │   │   │       │       │   │   │       │   ├── body3
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_mesh_black.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_mesh_grey.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_mesh_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_mesh_yellow.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_Normal_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_body3_Roughness_mesh_.jpg
│   │   │   │       │       │   │   │       │   ├── head1
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_mesh_black.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_mesh_grey.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_mesh_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_mesh_yellow.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_Normal_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_head1_Roughness_mesh_.jpg
│   │   │   │       │       │   │   │       │   ├── head2
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_mesh_black.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_mesh_grey.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_mesh_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_mesh_yellow.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_Normal_mesh_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_head2_Roughness_mesh_.jpg
│   │   │   │       │       │   │   │       │   └── head3
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_mesh_black.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_mesh_grey.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_mesh_orange.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_mesh_yellow.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_Normal_mesh_.jpg
│   │   │   │       │       │   │   │       │       └── T_head3_Roughness_mesh_.jpg
│   │   │   │       │       │   │   │       ├── metal
│   │   │   │       │       │   │   │       │   ├── backpack1
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_AmbientOcclusion_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_metal_blue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_metal_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_metal_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_metal_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Metalness_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Normal_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Opacity_metal_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_backpack1_Roughness_metal_.jpg
│   │   │   │       │       │   │   │       │   ├── backpack2
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_metal_blue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_metal_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_metal_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_metal_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Metalness_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Normal_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Opacity_metal_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_backpack2_Roughness_metal_.jpg
│   │   │   │       │       │   │   │       │   ├── backpack3
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_metal_blue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_metal_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_metal_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_metal_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Metalness_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Normal_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Opacity_metal_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_backpack3_Roughness_metal_.jpg
│   │   │   │       │       │   │   │       │   ├── body1
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_metal_blue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_metal_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_metal_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_metal_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_Metalness_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_Normal_metal_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_body1_Roughness_metal_.jpg
│   │   │   │       │       │   │   │       │   ├── body2
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_metal_blue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_metal_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_metal_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_metal_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_Metalness_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_Normal_metal_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_body2_Roughness_metal_.jpg
│   │   │   │       │       │   │   │       │   ├── body3
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_metal_blue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_metal_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_metal_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_metal_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_Metalness_metal_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_Normal_metal_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_body3_Roughness_metal_.jpg
│   │   │   │       │       │   │   │       │   ├── head1
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_metal_blue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_metal_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_metal_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_metal_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_Normal_metal_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_head1_Roughness_metal_.jpg
│   │   │   │       │       │   │   │       │   ├── head2
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_metal_blue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_metal_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_metal_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_metal_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_Normal_metal_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_head2_Roughness_metal_.jpg
│   │   │   │       │       │   │   │       │   └── head3
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_metal_blue.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_metal_green.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_metal_orange.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_metal_pink.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_Normal_metal_.jpg
│   │   │   │       │       │   │   │       │       └── T_head3_Roughness_metal_.jpg
│   │   │   │       │       │   │   │       ├── plastic
│   │   │   │       │       │   │   │       │   ├── backpack1
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_plastic_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_plastic_lightBlue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_plastic_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_BaseColor_plastic_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Metalness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Normal_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Opacity_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack1_Roughness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_backpack1_clearCoatMask_plastic_.jpg
│   │   │   │       │       │   │   │       │   ├── backpack2
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_plastic_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_plastic_lightBlue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_plastic_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_BaseColor_plastic_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Metalness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Normal_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Opacity_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack2_Roughness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_backpack2_clearCoatMask_plastic_.jpg
│   │   │   │       │       │   │   │       │   ├── backpack3
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_plastic_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_plastic_lightBlue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_plastic_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_BaseColor_plastic_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Metalness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Normal_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Opacity_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_backpack3_Roughness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_backpack3_clearCoatMask_plastic_.jpg
│   │   │   │       │       │   │   │       │   ├── body1
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_plastic_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_plastic_lightBlue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_plastic_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_BaseColor_plastic_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_Normal_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body1_Roughness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_body1_clearCoatMask_plastic_.jpg
│   │   │   │       │       │   │   │       │   ├── body2
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_plastic_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_plastic_lightBlue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_plastic_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_BaseColor_plastic_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_Normal_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body2_Roughness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_body2_clearCoatMask_plastic_.jpg
│   │   │   │       │       │   │   │       │   ├── body3
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_plastic_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_plastic_lightBlue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_plastic_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_BaseColor_plastic_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_Normal_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_body3_Roughness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_body3_clearCoatMask_plastic_.jpg
│   │   │   │       │       │   │   │       │   ├── head1
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_plastic_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_plastic_lightBlue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_plastic_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_BaseColor_plastic_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_Normal_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head1_Roughness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_head1_clearcoatMask_plastic_.jpg
│   │   │   │       │       │   │   │       │   ├── head2
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_plastic_green.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_plastic_lightBlue.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_plastic_orange.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_BaseColor_plastic_pink.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_Normal_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   ├── T_head2_Roughness_plastic_.jpg
│   │   │   │       │       │   │   │       │   │   └── T_head2_clearCoatMask_plastic_.jpg
│   │   │   │       │       │   │   │       │   └── head3
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_plastic_green.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_plastic_lightBlue.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_plastic_orange.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_BaseColor_plastic_pink.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_Normal_plastic_.jpg
│   │   │   │       │       │   │   │       │       ├── T_head3_Roughness_plastic_.jpg
│   │   │   │       │       │   │   │       │       └── T_head3_clearCoatMask_plastic_.jpg
│   │   │   │       │       │   │   │       └── rainbow
│   │   │   │       │       │   │   │           ├── backpack1
│   │   │   │       │       │   │   │           │   ├── T_backpack1_BaseColor_rainbow_beige.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack1_BaseColor_rainbow_black.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack1_BaseColor_rainbow_red.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack1_BaseColor_rainbow_rose.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack1_Metalness_rainbow_.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack1_Normal_rainbow_.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack1_Opacity_rainbow_.jpg
│   │   │   │       │       │   │   │           │   └── T_backpack1_Roughness_rainbow_.jpg
│   │   │   │       │       │   │   │           ├── backpack2
│   │   │   │       │       │   │   │           │   ├── T_backpack2_BaseColor_rainbow_beige.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack2_BaseColor_rainbow_black.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack2_BaseColor_rainbow_red.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack2_BaseColor_rainbow_rose.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack2_Metalness_rainbow_.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack2_Normal_rainbow_.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack2_Opacity_rainbow_.jpg
│   │   │   │       │       │   │   │           │   └── T_backpack2_Roughness_rainbow_.jpg
│   │   │   │       │       │   │   │           ├── backpack3
│   │   │   │       │       │   │   │           │   ├── T_backpack3_BaseColor_rainbow_beige.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack3_BaseColor_rainbow_black.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack3_BaseColor_rainbow_red.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack3_BaseColor_rainbow_rose.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack3_Metalness_rainbow_.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack3_Normal_rainbow_.jpg
│   │   │   │       │       │   │   │           │   ├── T_backpack3_Opacity_rainbow_.jpg
│   │   │   │       │       │   │   │           │   └── T_backpack3_Roughness_rainbow_.jpg
│   │   │   │       │       │   │   │           ├── body1
│   │   │   │       │       │   │   │           │   ├── T_body1_BaseColor_rainbow_beige.jpg
│   │   │   │       │       │   │   │           │   ├── T_body1_BaseColor_rainbow_black.jpg
│   │   │   │       │       │   │   │           │   ├── T_body1_BaseColor_rainbow_red.jpg
│   │   │   │       │       │   │   │           │   ├── T_body1_BaseColor_rainbow_rose.jpg
│   │   │   │       │       │   │   │           │   ├── T_body1_Normal_rainbow_.jpg
│   │   │   │       │       │   │   │           │   └── T_body1_Roughness_rainbow_.jpg
│   │   │   │       │       │   │   │           ├── body2
│   │   │   │       │       │   │   │           │   ├── T_body2_BaseColor_rainbow_beige.jpg
│   │   │   │       │       │   │   │           │   ├── T_body2_BaseColor_rainbow_black.jpg
│   │   │   │       │       │   │   │           │   ├── T_body2_BaseColor_rainbow_red.jpg
│   │   │   │       │       │   │   │           │   ├── T_body2_BaseColor_rainbow_rose.jpg
│   │   │   │       │       │   │   │           │   ├── T_body2_Normal_rainbow_.jpg
│   │   │   │       │       │   │   │           │   └── T_body2_Roughness_rainbow_.jpg
│   │   │   │       │       │   │   │           ├── body3
│   │   │   │       │       │   │   │           │   ├── T_body3_BaseColor_rainbow_beige.jpg
│   │   │   │       │       │   │   │           │   ├── T_body3_BaseColor_rainbow_black.jpg
│   │   │   │       │       │   │   │           │   ├── T_body3_BaseColor_rainbow_red.jpg
│   │   │   │       │       │   │   │           │   ├── T_body3_BaseColor_rainbow_rose.jpg
│   │   │   │       │       │   │   │           │   ├── T_body3_Normal_rainbow_.jpg
│   │   │   │       │       │   │   │           │   └── T_body3_Roughness_rainbow_.jpg
│   │   │   │       │       │   │   │           ├── head1
│   │   │   │       │       │   │   │           │   ├── T_head1_BaseColor_rainbow_beige.jpg
│   │   │   │       │       │   │   │           │   ├── T_head1_BaseColor_rainbow_black.jpg
│   │   │   │       │       │   │   │           │   ├── T_head1_BaseColor_rainbow_red.jpg
│   │   │   │       │       │   │   │           │   ├── T_head1_BaseColor_rainbow_rose.jpg
│   │   │   │       │       │   │   │           │   ├── T_head1_Normal_rainbow_.jpg
│   │   │   │       │       │   │   │           │   └── T_head1_Roughness_rainbow_.jpg
│   │   │   │       │       │   │   │           ├── head2
│   │   │   │       │       │   │   │           │   ├── T_head2_BaseColor_rainbow_beige.jpg
│   │   │   │       │       │   │   │           │   ├── T_head2_BaseColor_rainbow_black.jpg
│   │   │   │       │       │   │   │           │   ├── T_head2_BaseColor_rainbow_red.jpg
│   │   │   │       │       │   │   │           │   ├── T_head2_BaseColor_rainbow_rose.jpg
│   │   │   │       │       │   │   │           │   ├── T_head2_Normal_rainbow_.jpg
│   │   │   │       │       │   │   │           │   └── T_head2_Roughness_rainbow_.jpg
│   │   │   │       │       │   │   │           └── head3
│   │   │   │       │       │   │   │               ├── T_head3_BaseColor_rainbow_beige.jpg
│   │   │   │       │       │   │   │               ├── T_head3_BaseColor_rainbow_black.jpg
│   │   │   │       │       │   │   │               ├── T_head3_BaseColor_rainbow_red.jpg
│   │   │   │       │       │   │   │               ├── T_head3_BaseColor_rainbow_rose.jpg
│   │   │   │       │       │   │   │               ├── T_head3_Normal_rainbow_.jpg
│   │   │   │       │       │   │   │               └── T_head3_Roughness_rainbow_.jpg
│   │   │   │       │       │   │   ├── environment
│   │   │   │       │       │   │   │   ├── mesh
│   │   │   │       │       │   │   │   │   └── volume.usd
│   │   │   │       │       │   │   │   └── textures
│   │   │   │       │       │   │   │       ├── T_dirt_AmbientOcclusion.jpg
│   │   │   │       │       │   │   │       ├── T_dirt_BaseColor.jpg
│   │   │   │       │       │   │   │       ├── T_dirt_Height.jpg
│   │   │   │       │       │   │   │       ├── T_dirt_Normal.jpg
│   │   │   │       │       │   │   │       ├── T_dirt_Roughness.jpg
│   │   │   │       │       │   │   │       ├── T_islandBase_BaseColor.jpg
│   │   │   │       │       │   │   │       ├── T_islandBase_Normal.jpg
│   │   │   │       │       │   │   │       ├── T_islandBase_Roughness.jpg
│   │   │   │       │       │   │   │       ├── T_islandEdge_BaseColor.jpg
│   │   │   │       │       │   │   │       ├── T_islandEdge_Metalness.jpg
│   │   │   │       │       │   │   │       ├── T_islandEdge_Normal.jpg
│   │   │   │       │       │   │   │       ├── T_islandEdge_Roughness.jpg
│   │   │   │       │       │   │   │       ├── T_islandTop_BaseColor.jpg
│   │   │   │       │       │   │   │       ├── T_islandTop_Normal.jpg
│   │   │   │       │       │   │   │       ├── T_islandTop_Roughness.jpg
│   │   │   │       │       │   │   │       ├── T_planters_BaseColor.jpg
│   │   │   │       │       │   │   │       ├── T_planters_Metalness.jpg
│   │   │   │       │       │   │   │       ├── T_planters_Normal.jpg
│   │   │   │       │       │   │   │       ├── T_planters_Roughness.jpg
│   │   │   │       │       │   │   │       └── T_planters_circle_mask.jpg
│   │   │   │       │       │   │   └── plants
│   │   │   │       │       │   │       ├── animations
│   │   │   │       │       │   │       │   ├── coffeeBerry_celebrate_anim.usdz
│   │   │   │       │       │   │       │   ├── coffeeBerry_grow_anim.usdz
│   │   │   │       │       │   │       │   ├── poppy_celebrate_anim.usdz
│   │   │   │       │       │   │       │   ├── poppy_grow_anim.usdz
│   │   │   │       │       │   │       │   ├── yucca_celebrate_anim.usdz
│   │   │   │       │       │   │       │   └── yucca_grow_anim.usdz
│   │   │   │       │       │   │       ├── mesh
│   │   │   │       │       │   │       │   ├── hero
│   │   │   │       │       │   │       │   │   ├── coffeeBerry.usdz
│   │   │   │       │       │   │       │   │   ├── poppy.usdz
│   │   │   │       │       │   │       │   │   └── yucca.usdz
│   │   │   │       │       │   │       │   └── setDressing
│   │   │   │       │       │   │       │       ├── bottomSetDressing.usd
│   │   │   │       │       │   │       │       └── foliageSetDressing.usd
│   │   │   │       │       │   │       └── textures
│   │   │   │       │       │   │           ├── T_bigPlant_BaseColor.jpg
│   │   │   │       │       │   │           ├── T_bigPlant_Emissive.jpg
│   │   │   │       │       │   │           ├── T_bigPlant_Normal.jpg
│   │   │   │       │       │   │           ├── T_bigPlant_Roughness.jpg
│   │   │   │       │       │   │           ├── T_bigPlant_bulb_mask.jpg
│   │   │   │       │       │   │           ├── T_bigPlant_emissive2_mask.jpg
│   │   │   │       │       │   │           ├── T_bigPlant_emissive_mask.jpg
│   │   │   │       │       │   │           ├── T_coffeeBerry_BaseColor.jpg
│   │   │   │       │       │   │           ├── T_coffeeBerry_Emissive.jpg
│   │   │   │       │       │   │           ├── T_coffeeBerry_Normal.jpg
│   │   │   │       │       │   │           ├── T_coffeeBerry_Roughness.jpg
│   │   │   │       │       │   │           ├── T_coffeeBerry_berry_mask.jpg
│   │   │   │       │       │   │           ├── T_coffeeberry_upLight_mask.jpg
│   │   │   │       │       │   │           ├── T_poppy_BaseColor.jpg
│   │   │   │       │       │   │           ├── T_poppy_Emissive.jpg
│   │   │   │       │       │   │           ├── T_poppy_Mask.jpg
│   │   │   │       │       │   │           ├── T_poppy_Normal.jpg
│   │   │   │       │       │   │           ├── T_poppy_Roughness.jpg
│   │   │   │       │       │   │           ├── T_poppy_emissiveMask.jpg
│   │   │   │       │       │   │           ├── T_poppy_upLight_mask.jpg
│   │   │   │       │       │   │           ├── T_sidePlant_BaseColor.jpg
│   │   │   │       │       │   │           ├── T_sidePlant_Normal.jpg
│   │   │   │       │       │   │           ├── T_sidePlant_Roughness.jpg
│   │   │   │       │       │   │           ├── T_sidePlant_curvature_mask.jpg
│   │   │   │       │       │   │           ├── T_sidePlant_emissive_mask.jpg
│   │   │   │       │       │   │           ├── T_yucca_BaseColor.jpg
│   │   │   │       │       │   │           ├── T_yucca_Emissive.jpg
│   │   │   │       │       │   │           ├── T_yucca_Normal.jpg
│   │   │   │       │       │   │           ├── T_yucca_Roughness.jpg
│   │   │   │       │       │   │           ├── T_yucca_emissive_mask.jpg
│   │   │   │       │       │   │           ├── T_yucca_upLight_mask.jpg
│   │   │   │       │       │   │           ├── poppyThickness_mask.jpg
│   │   │   │       │       │   │           └── sideplant_EmmissiveMask.jpg
│   │   │   │       │       │   ├── Materials
│   │   │   │       │       │   │   ├── M_environment.usda
│   │   │   │       │       │   │   ├── M_face.usda
│   │   │   │       │       │   │   ├── M_lights.usda
│   │   │   │       │       │   │   ├── M_mesh.usda
│   │   │   │       │       │   │   ├── M_metal.usda
│   │   │   │       │       │   │   ├── M_plants.usda
│   │   │   │       │       │   │   ├── M_plastic.usda
│   │   │   │       │       │   │   └── M_rainbow.usda
│   │   │   │       │       │   └── scenes
│   │   │   │       │       │       ├── backpack1.usda
│   │   │   │       │       │       ├── backpack2.usda
│   │   │   │       │       │       ├── backpack3.usda
│   │   │   │       │       │       ├── body1.usda
│   │   │   │       │       │       ├── body2.usda
│   │   │   │       │       │       ├── body3.usda
│   │   │   │       │       │       ├── head1.usda
│   │   │   │       │       │       ├── head2.usda
│   │   │   │       │       │       ├── head3.usda
│   │   │   │       │       │       ├── lighting.usda
│   │   │   │       │       │       ├── planter_Hero.usda
│   │   │   │       │       │       ├── setDressing.usda
│   │   │   │       │       │       └── volume.usda
│   │   │   │       │       ├── Components
│   │   │   │       │       │   └── PlantComponent.swift
│   │   │   │       │       ├── Extensions
│   │   │   │       │       │   └── EntityExtensions.swift
│   │   │   │       │       └── BOTanistAssets.swift
│   │   │   │       └── Package.swift
│   │   │   ├── LICENSE.txt
│   │   │   ├── README.md
│   │   │   └── metadata.json
│   │   ├── building-an-immersive-media-viewing-experience
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── DestinationVideo
│   │   │   │   ├── Extensions
│   │   │   │   │   ├── AVExtensions.swift
│   │   │   │   │   ├── DestinationVideoExtensions.swift
│   │   │   │   │   └── MultiplatformExtensions.swift
│   │   │   │   ├── Model
│   │   │   │   │   ├── Data
│   │   │   │   │   │   ├── Genre.swift
│   │   │   │   │   │   ├── Importer.swift
│   │   │   │   │   │   ├── Person.swift
│   │   │   │   │   │   ├── PreviewData.swift
│   │   │   │   │   │   ├── RelationshipMapping.swift
│   │   │   │   │   │   ├── SampleData.swift
│   │   │   │   │   │   ├── UpNextItem.swift
│   │   │   │   │   │   └── Video.swift
│   │   │   │   │   ├── visionOS
│   │   │   │   │   │   ├── EnvironmentStateHandler.swift
│   │   │   │   │   │   └── ImmersiveEnvironment.swift
│   │   │   │   │   ├── Category.swift
│   │   │   │   │   ├── Constants.swift
│   │   │   │   │   ├── NavigationNode.swift
│   │   │   │   │   └── Tabs.swift
│   │   │   │   ├── Player
│   │   │   │   │   ├── InlinePlayerView.swift
│   │   │   │   │   ├── PlayerModel.swift
│   │   │   │   │   ├── PlayerView.swift
│   │   │   │   │   ├── SystemPlayerView.swift
│   │   │   │   │   └── UpNextView.swift
│   │   │   │   ├── Preview Content
│   │   │   │   │   └── Preview Assets.xcassets
│   │   │   │   │       └── Contents.json
│   │   │   │   ├── Resources
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AccentColor.colorset
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── AppIcon.appiconset
│   │   │   │   │   │   │   ├── AppIcon.png
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   ├── DarkAppIcon.png
│   │   │   │   │   │   │   ├── TintableAppIcon.png
│   │   │   │   │   │   │   ├── icon_128x128.png
│   │   │   │   │   │   │   ├── icon_128x128@2x.png
│   │   │   │   │   │   │   ├── icon_16x16.png
│   │   │   │   │   │   │   ├── icon_16x16@2x.png
│   │   │   │   │   │   │   ├── icon_256x256.png
│   │   │   │   │   │   │   ├── icon_256x256@2x.png
│   │   │   │   │   │   │   ├── icon_32x32.png
│   │   │   │   │   │   │   ├── icon_32x32@2x.png
│   │   │   │   │   │   │   ├── icon_512x512.png
│   │   │   │   │   │   │   └── icon_512x512@2x.png
│   │   │   │   │   │   ├── AppIcon.brandassets
│   │   │   │   │   │   │   ├── App Icon - App Store.imagestack
│   │   │   │   │   │   │   │   ├── Back.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   ├── Front.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   ├── Middle.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── App Icon.imagestack
│   │   │   │   │   │   │   │   ├── Back.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   ├── Back.png
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   ├── Front.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   │   │   └── Front.png
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   ├── Middle.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Top Shelf Image Wide.imageset
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Top Shelf Image.imageset
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   ├── Back.png
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   │   └── Front.png
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── BOT-anist_landscape.imageset
│   │   │   │   │   │   │   ├── BOT-anist_landscape.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── BOT-anist_portrait.imageset
│   │   │   │   │   │   │   ├── BOT-anist_portrait.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── amazing_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── amazing-animation-poster.png
│   │   │   │   │   │   ├── animals_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── cute-animals-poster.png
│   │   │   │   │   │   ├── beach_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── beach_landscape.png
│   │   │   │   │   │   ├── beach_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── beach_portrait.png
│   │   │   │   │   │   ├── camping_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── camping_landscape.png
│   │   │   │   │   │   ├── camping_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── camping_portrait.png
│   │   │   │   │   │   ├── cinematic_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── cinematic_poster.png
│   │   │   │   │   │   ├── creek_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── creek_landscape.png
│   │   │   │   │   │   ├── creek_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── creek_portrait.png
│   │   │   │   │   │   ├── dance_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── dance_landscape.png
│   │   │   │   │   │   ├── dance_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── dance_portrait.png
│   │   │   │   │   │   ├── discovery_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── discovery_landscape.png
│   │   │   │   │   │   ├── discovery_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── discovery_portrait.png
│   │   │   │   │   │   ├── dv_logo.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── dv_logo@2x.png
│   │   │   │   │   │   ├── extraordinary_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── extraordinary-poster.png
│   │   │   │   │   │   ├── forest_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── forest_poster.png
│   │   │   │   │   │   ├── hillside_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── hillside_landscape.png
│   │   │   │   │   │   ├── hillside_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── hillside_portrait.png
│   │   │   │   │   │   ├── lab_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── lab_landscape.png
│   │   │   │   │   │   ├── lab_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── lab_portrait.png
│   │   │   │   │   │   ├── lake_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── lake_landscape.png
│   │   │   │   │   │   ├── lake_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── lake_portrait.png
│   │   │   │   │   │   ├── landing_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── landing_landscape.png
│   │   │   │   │   │   ├── landing_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── landing_portriat.png
│   │   │   │   │   │   ├── ocean_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── ocean_landscape.png
│   │   │   │   │   │   ├── ocean_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── ocean_portrait.png
│   │   │   │   │   │   ├── park_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── park_landscape.png
│   │   │   │   │   │   ├── park_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── park_portrait.png
│   │   │   │   │   │   ├── samples_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── samples_landscape.png
│   │   │   │   │   │   ├── samples_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── samples_portriat.png
│   │   │   │   │   │   ├── sea_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── by-the-sea-poster.png
│   │   │   │   │   │   ├── studio_thumbnail_dark.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── studio_thumbnail_dark.png
│   │   │   │   │   │   ├── studio_thumbnail_light.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── studio_thumbnail_light.png
│   │   │   │   │   │   ├── tvBackground.colorset
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Videos
│   │   │   │   │   │   ├── BOT-anist_video.mov
│   │   │   │   │   │   └── dance_video.mov
│   │   │   │   │   ├── de.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── fr.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── hi.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── ja.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── ko.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── zh_CN.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   └── Localizable.xcstrings
│   │   │   │   ├── SharePlay
│   │   │   │   │   ├── WatchingActivity.swift
│   │   │   │   │   └── WatchingCoordinator.swift
│   │   │   │   ├── Views
│   │   │   │   │   ├── visionOS
│   │   │   │   │   │   ├── ImmersiveEnvironmentPickerView.swift
│   │   │   │   │   │   ├── ImmersiveEnvironmentView.swift
│   │   │   │   │   │   ├── ProfileButton.swift
│   │   │   │   │   │   └── TrailerView.swift
│   │   │   │   │   ├── ButtonStyle.swift
│   │   │   │   │   ├── CategoryListView.swift
│   │   │   │   │   ├── CategoryView.swift
│   │   │   │   │   ├── DetailView.swift
│   │   │   │   │   ├── GradientView.swift
│   │   │   │   │   ├── HeroView.swift
│   │   │   │   │   ├── LibraryView.swift
│   │   │   │   │   ├── VideoCardView.swift
│   │   │   │   │   ├── VideoInfoView.swift
│   │   │   │   │   ├── VideoListView.swift
│   │   │   │   │   ├── ViewModifiers.swift
│   │   │   │   │   └── WatchNowView.swift
│   │   │   │   ├── ContentView.swift
│   │   │   │   ├── DestinationTabs.swift
│   │   │   │   ├── DestinationVideo.entitlements
│   │   │   │   ├── DestinationVideo.swift
│   │   │   │   ├── Info.plist
│   │   │   │   └── PlayerWindow.swift
│   │   │   ├── DestinationVideo.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── Packages
│   │   │   │   └── Studio
│   │   │   │       ├── Package.realitycomposerpro
│   │   │   │       │   ├── ProjectData
│   │   │   │       │   │   └── main.json
│   │   │   │       │   └── WorkspaceData
│   │   │   │       │       ├── SceneMetadataList.json
│   │   │   │       │       └── Settings.rcprojectdata
│   │   │   │       ├── Sources
│   │   │   │       │   └── Studio
│   │   │   │       │       ├── Studio.rkassets
│   │   │   │       │       │   ├── ibl
│   │   │   │       │       │   │   ├── Studio_IBL_LatLong_Dark.exr
│   │   │   │       │       │   │   └── Studio_IBL_LatLong_Light.exr
│   │   │   │       │       │   ├── meshes
│   │   │   │       │       │   │   ├── Studio.usdc
│   │   │   │       │       │   │   ├── Studio_floor_2_2_Lightspill.usdc
│   │   │   │       │       │   │   ├── Studio_floor_2_Lightspill.usdc
│   │   │   │       │       │   │   └── dome.usdc
│   │   │   │       │       │   ├── scenes
│   │   │   │       │       │   │   ├── Common.usda
│   │   │   │       │       │   │   ├── Floor.usda
│   │   │   │       │       │   │   ├── StudioDark.usda
│   │   │   │       │       │   │   └── StudioLight.usda
│   │   │   │       │       │   ├── textures
│   │   │   │       │       │   │   ├── common
│   │   │   │       │       │   │   │   └── DefaultAttenuationMap.exr
│   │   │   │       │       │   │   ├── dark
│   │   │   │       │       │   │   │   ├── BakingGroup1_1_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup1_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup2_2_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup2_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup3_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup4_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup5_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup6_d.png
│   │   │   │       │       │   │   │   └── BakingGroup7_d.png
│   │   │   │       │       │   │   ├── light
│   │   │   │       │       │   │   │   ├── BakingGroup1.png
│   │   │   │       │       │   │   │   ├── BakingGroup1_1.png
│   │   │   │       │       │   │   │   ├── BakingGroup2.png
│   │   │   │       │       │   │   │   ├── BakingGroup2_2.png
│   │   │   │       │       │   │   │   ├── BakingGroup3.png
│   │   │   │       │       │   │   │   ├── BakingGroup4.png
│   │   │   │       │       │   │   │   ├── BakingGroup5.png
│   │   │   │       │       │   │   │   ├── BakingGroup6.png
│   │   │   │       │       │   │   │   └── BakingGroup7.png
│   │   │   │       │       │   │   └── skies
│   │   │   │       │       │   │       ├── Studio_sky_LatLong_Dark.exr
│   │   │   │       │       │   │       └── Studio_sky_LatLong_Light.exr
│   │   │   │       │       │   └── AAA_MainScene.usda
│   │   │   │       │       └── Studio.swift
│   │   │   │       └── Package.swift
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── building-local-experiences-with-room-tracking
│   │   │   ├── ARKitRoomTracking
│   │   │   │   ├── ARKitRoomTrackingApp.swift
│   │   │   │   ├── AppState.swift
│   │   │   │   ├── ContentView.swift
│   │   │   │   ├── Extensions.swift
│   │   │   │   ├── Info.plist
│   │   │   │   └── WorldAndRoomView.swift
│   │   │   ├── ARKitRoomTracking.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── ARKitRoomTracking.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── combining-2d-and-3d-views-in-an-immersive-app
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── MultiDimensionalImmersiveContent
│   │   │   │   ├── Assets.xcassets
│   │   │   │   │   ├── AppIcon.appiconset
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   └── Contents.json
│   │   │   │   ├── CALayerArch
│   │   │   │   │   ├── CALayerArcRepresentable.swift
│   │   │   │   │   └── CALayerArcView.swift
│   │   │   │   ├── Preview Content
│   │   │   │   │   └── Preview Assets.xcassets
│   │   │   │   │       └── Contents.json
│   │   │   │   ├── SwiftUIArch
│   │   │   │   │   └── SwiftUIArcView.swift
│   │   │   │   ├── UIViewArch
│   │   │   │   │   ├── UIViewArcRepresentable.swift
│   │   │   │   │   └── UIViewArcView.swift
│   │   │   │   ├── Extensions.swift
│   │   │   │   ├── Info.plist
│   │   │   │   ├── MultiDimensionalImmersiveContentApp.swift
│   │   │   │   ├── RainbowModel.swift
│   │   │   │   └── RainbowView.swift
│   │   │   ├── MultiDimensionalImmersiveContent.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       ├── xcschemes
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── MultiDimensionalImmersiveContent.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── Packages
│   │   │   │   └── RealityKitContent
│   │   │   │       ├── Package.realitycomposerpro
│   │   │   │       │   ├── ProjectData
│   │   │   │       │   │   └── main.json
│   │   │   │       │   └── WorkspaceData
│   │   │   │       │       ├── SceneMetadataList.json
│   │   │   │       │       └── Settings.rcprojectdata
│   │   │   │       ├── Sources
│   │   │   │       │   └── RealityKitContent
│   │   │   │       │       ├── RealityKitContent.rkassets
│   │   │   │       │       │   ├── Materials
│   │   │   │       │       │   │   └── GreenMaterial.usda
│   │   │   │       │       │   ├── green.usdc
│   │   │   │       │       │   ├── plane.usdc
│   │   │   │       │       │   └── yellow.usdc
│   │   │   │       │       └── RealityKitContent.swift
│   │   │   │       ├── Package.swift
│   │   │   │       └── README.md
│   │   │   ├── LICENSE.txt
│   │   │   ├── README.md
│   │   │   └── metadata.json
│   │   ├── creating-3d-entities-with-realitykit
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── Creating 3D Shapes
│   │   │   │   ├── App
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── EntryPoint.swift
│   │   │   │   │   └── Info.plist
│   │   │   │   ├── Entities
│   │   │   │   │   └── ShapesView+Entities.swift
│   │   │   │   └── Views
│   │   │   │       └── ShapesView.swift
│   │   │   ├── Creating 3D Shapes.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── 3D Shapes.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   ├── README.md
│   │   │   └── metadata.json
│   │   ├── creating-an-interactive-3d-model-in-visionos
│   │   │   ├── CarExample
│   │   │   │   ├── App
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── EntryPoint.swift
│   │   │   │   │   └── Info.plist
│   │   │   │   ├── Extensions
│   │   │   │   │   └── SIMD3.swift
│   │   │   │   ├── Resources
│   │   │   │   │   └── Huracan-EVO-RWD-Spyder-opt-22.usdz
│   │   │   │   └── Views
│   │   │   │       ├── CarView.swift
│   │   │   │       └── MainView.swift
│   │   │   ├── CarExample.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── LICENSE.txt
│   │   │   ├── README.md
│   │   │   └── metadata.json
│   │   ├── destination-video
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── DestinationVideo
│   │   │   │   ├── Extensions
│   │   │   │   │   ├── AVExtensions.swift
│   │   │   │   │   ├── DestinationVideoExtensions.swift
│   │   │   │   │   └── MultiplatformExtensions.swift
│   │   │   │   ├── Model
│   │   │   │   │   ├── Data
│   │   │   │   │   │   ├── Genre.swift
│   │   │   │   │   │   ├── Importer.swift
│   │   │   │   │   │   ├── Person.swift
│   │   │   │   │   │   ├── PreviewData.swift
│   │   │   │   │   │   ├── RelationshipMapping.swift
│   │   │   │   │   │   ├── SampleData.swift
│   │   │   │   │   │   ├── UpNextItem.swift
│   │   │   │   │   │   └── Video.swift
│   │   │   │   │   ├── visionOS
│   │   │   │   │   │   ├── EnvironmentStateHandler.swift
│   │   │   │   │   │   └── ImmersiveEnvironment.swift
│   │   │   │   │   ├── Category.swift
│   │   │   │   │   ├── Constants.swift
│   │   │   │   │   ├── NavigationNode.swift
│   │   │   │   │   └── Tabs.swift
│   │   │   │   ├── Player
│   │   │   │   │   ├── InlinePlayerView.swift
│   │   │   │   │   ├── PlayerModel.swift
│   │   │   │   │   ├── PlayerView.swift
│   │   │   │   │   ├── SystemPlayerView.swift
│   │   │   │   │   └── UpNextView.swift
│   │   │   │   ├── Preview Content
│   │   │   │   │   └── Preview Assets.xcassets
│   │   │   │   │       └── Contents.json
│   │   │   │   ├── Resources
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AccentColor.colorset
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── AppIcon.appiconset
│   │   │   │   │   │   │   ├── AppIcon.png
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   ├── DarkAppIcon.png
│   │   │   │   │   │   │   ├── TintableAppIcon.png
│   │   │   │   │   │   │   ├── icon_128x128.png
│   │   │   │   │   │   │   ├── icon_128x128@2x.png
│   │   │   │   │   │   │   ├── icon_16x16.png
│   │   │   │   │   │   │   ├── icon_16x16@2x.png
│   │   │   │   │   │   │   ├── icon_256x256.png
│   │   │   │   │   │   │   ├── icon_256x256@2x.png
│   │   │   │   │   │   │   ├── icon_32x32.png
│   │   │   │   │   │   │   ├── icon_32x32@2x.png
│   │   │   │   │   │   │   ├── icon_512x512.png
│   │   │   │   │   │   │   └── icon_512x512@2x.png
│   │   │   │   │   │   ├── AppIcon.brandassets
│   │   │   │   │   │   │   ├── App Icon - App Store.imagestack
│   │   │   │   │   │   │   │   ├── Back.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   ├── Front.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   ├── Middle.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── App Icon.imagestack
│   │   │   │   │   │   │   │   ├── Back.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   ├── Back.png
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   ├── Front.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   │   │   └── Front.png
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   ├── Middle.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Top Shelf Image Wide.imageset
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Top Shelf Image.imageset
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   ├── Back.png
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   │   └── Front.png
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── BOT-anist_landscape.imageset
│   │   │   │   │   │   │   ├── BOT-anist_landscape.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── BOT-anist_portrait.imageset
│   │   │   │   │   │   │   ├── BOT-anist_portrait.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── amazing_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── amazing-animation-poster.png
│   │   │   │   │   │   ├── animals_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── cute-animals-poster.png
│   │   │   │   │   │   ├── beach_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── beach_landscape.png
│   │   │   │   │   │   ├── beach_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── beach_portrait.png
│   │   │   │   │   │   ├── camping_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── camping_landscape.png
│   │   │   │   │   │   ├── camping_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── camping_portrait.png
│   │   │   │   │   │   ├── cinematic_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── cinematic_poster.png
│   │   │   │   │   │   ├── creek_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── creek_landscape.png
│   │   │   │   │   │   ├── creek_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── creek_portrait.png
│   │   │   │   │   │   ├── dance_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── dance_landscape.png
│   │   │   │   │   │   ├── dance_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── dance_portrait.png
│   │   │   │   │   │   ├── discovery_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── discovery_landscape.png
│   │   │   │   │   │   ├── discovery_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── discovery_portrait.png
│   │   │   │   │   │   ├── dv_logo.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── dv_logo@2x.png
│   │   │   │   │   │   ├── extraordinary_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── extraordinary-poster.png
│   │   │   │   │   │   ├── forest_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── forest_poster.png
│   │   │   │   │   │   ├── hillside_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── hillside_landscape.png
│   │   │   │   │   │   ├── hillside_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── hillside_portrait.png
│   │   │   │   │   │   ├── lab_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── lab_landscape.png
│   │   │   │   │   │   ├── lab_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── lab_portrait.png
│   │   │   │   │   │   ├── lake_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── lake_landscape.png
│   │   │   │   │   │   ├── lake_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── lake_portrait.png
│   │   │   │   │   │   ├── landing_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── landing_landscape.png
│   │   │   │   │   │   ├── landing_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── landing_portriat.png
│   │   │   │   │   │   ├── ocean_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── ocean_landscape.png
│   │   │   │   │   │   ├── ocean_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── ocean_portrait.png
│   │   │   │   │   │   ├── park_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── park_landscape.png
│   │   │   │   │   │   ├── park_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── park_portrait.png
│   │   │   │   │   │   ├── samples_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── samples_landscape.png
│   │   │   │   │   │   ├── samples_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── samples_portriat.png
│   │   │   │   │   │   ├── sea_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── by-the-sea-poster.png
│   │   │   │   │   │   ├── studio_thumbnail_dark.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── studio_thumbnail_dark.png
│   │   │   │   │   │   ├── studio_thumbnail_light.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── studio_thumbnail_light.png
│   │   │   │   │   │   ├── tvBackground.colorset
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Videos
│   │   │   │   │   │   ├── BOT-anist_video.mov
│   │   │   │   │   │   └── dance_video.mov
│   │   │   │   │   ├── de.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── fr.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── hi.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── ja.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── ko.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── zh_CN.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   └── Localizable.xcstrings
│   │   │   │   ├── SharePlay
│   │   │   │   │   ├── WatchingActivity.swift
│   │   │   │   │   └── WatchingCoordinator.swift
│   │   │   │   ├── Views
│   │   │   │   │   ├── visionOS
│   │   │   │   │   │   ├── ImmersiveEnvironmentPickerView.swift
│   │   │   │   │   │   ├── ImmersiveEnvironmentView.swift
│   │   │   │   │   │   ├── ProfileButton.swift
│   │   │   │   │   │   └── TrailerView.swift
│   │   │   │   │   ├── ButtonStyle.swift
│   │   │   │   │   ├── CategoryListView.swift
│   │   │   │   │   ├── CategoryView.swift
│   │   │   │   │   ├── DetailView.swift
│   │   │   │   │   ├── GradientView.swift
│   │   │   │   │   ├── HeroView.swift
│   │   │   │   │   ├── LibraryView.swift
│   │   │   │   │   ├── VideoCardView.swift
│   │   │   │   │   ├── VideoInfoView.swift
│   │   │   │   │   ├── VideoListView.swift
│   │   │   │   │   ├── ViewModifiers.swift
│   │   │   │   │   └── WatchNowView.swift
│   │   │   │   ├── ContentView.swift
│   │   │   │   ├── DestinationTabs.swift
│   │   │   │   ├── DestinationVideo.entitlements
│   │   │   │   ├── DestinationVideo.swift
│   │   │   │   ├── Info.plist
│   │   │   │   └── PlayerWindow.swift
│   │   │   ├── DestinationVideo.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── Packages
│   │   │   │   └── Studio
│   │   │   │       ├── Package.realitycomposerpro
│   │   │   │       │   ├── ProjectData
│   │   │   │       │   │   └── main.json
│   │   │   │       │   └── WorkspaceData
│   │   │   │       │       ├── SceneMetadataList.json
│   │   │   │       │       └── Settings.rcprojectdata
│   │   │   │       ├── Sources
│   │   │   │       │   └── Studio
│   │   │   │       │       ├── Studio.rkassets
│   │   │   │       │       │   ├── ibl
│   │   │   │       │       │   │   ├── Studio_IBL_LatLong_Dark.exr
│   │   │   │       │       │   │   └── Studio_IBL_LatLong_Light.exr
│   │   │   │       │       │   ├── meshes
│   │   │   │       │       │   │   ├── Studio.usdc
│   │   │   │       │       │   │   ├── Studio_floor_2_2_Lightspill.usdc
│   │   │   │       │       │   │   ├── Studio_floor_2_Lightspill.usdc
│   │   │   │       │       │   │   └── dome.usdc
│   │   │   │       │       │   ├── scenes
│   │   │   │       │       │   │   ├── Common.usda
│   │   │   │       │       │   │   ├── Floor.usda
│   │   │   │       │       │   │   ├── StudioDark.usda
│   │   │   │       │       │   │   └── StudioLight.usda
│   │   │   │       │       │   ├── textures
│   │   │   │       │       │   │   ├── common
│   │   │   │       │       │   │   │   └── DefaultAttenuationMap.exr
│   │   │   │       │       │   │   ├── dark
│   │   │   │       │       │   │   │   ├── BakingGroup1_1_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup1_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup2_2_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup2_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup3_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup4_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup5_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup6_d.png
│   │   │   │       │       │   │   │   └── BakingGroup7_d.png
│   │   │   │       │       │   │   ├── light
│   │   │   │       │       │   │   │   ├── BakingGroup1.png
│   │   │   │       │       │   │   │   ├── BakingGroup1_1.png
│   │   │   │       │       │   │   │   ├── BakingGroup2.png
│   │   │   │       │       │   │   │   ├── BakingGroup2_2.png
│   │   │   │       │       │   │   │   ├── BakingGroup3.png
│   │   │   │       │       │   │   │   ├── BakingGroup4.png
│   │   │   │       │       │   │   │   ├── BakingGroup5.png
│   │   │   │       │       │   │   │   ├── BakingGroup6.png
│   │   │   │       │       │   │   │   └── BakingGroup7.png
│   │   │   │       │       │   │   └── skies
│   │   │   │       │       │   │       ├── Studio_sky_LatLong_Dark.exr
│   │   │   │       │       │   │       └── Studio_sky_LatLong_Light.exr
│   │   │   │       │       │   └── AAA_MainScene.usda
│   │   │   │       │       └── Studio.swift
│   │   │   │       └── Package.swift
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── diorama
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── Diorama
│   │   │   │   ├── Assets.xcassets
│   │   │   │   │   ├── AccentColor.colorset
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   └── diorama-icon-bottom.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   └── diorama-export-top.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   └── diorama-icon-middle.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Flowers_14_Yellow.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── Flowers_14_Yellow.jpeg
│   │   │   │   │   ├── Landscape_22_Sailboats.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── Landscape_22_Sailboats.jpeg
│   │   │   │   │   ├── Landscape_25_Tropical_Sunset_Palms.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── Landscape_25_Tropical_Sunset_Palms.jpeg
│   │   │   │   │   ├── Landscape_28_Purple_Sky.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── Landscape_28_Purple_Sky.jpeg
│   │   │   │   │   ├── Landscape_29_Tropical_Sunset_Boat.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── Landscape_29_Tropical_Sunset_Boat.jpeg
│   │   │   │   │   ├── Landscape_2_Sunset.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── Landscape_2_Sunset.jpeg
│   │   │   │   │   ├── Landscape_33_Trees_Rocks.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── Landscape_33_Trees_Rocks.jpeg
│   │   │   │   │   └── Contents.json
│   │   │   │   ├── Preview Content
│   │   │   │   │   └── Preview Assets.xcassets
│   │   │   │   │       └── Contents.json
│   │   │   │   ├── AttachmentsProvider.swift
│   │   │   │   ├── Components.swift
│   │   │   │   ├── ContentView.swift
│   │   │   │   ├── DioramaApp.swift
│   │   │   │   ├── DioramaView.swift
│   │   │   │   ├── FlockingComponent.swift
│   │   │   │   ├── FlockingSystem.swift
│   │   │   │   ├── Info.plist
│   │   │   │   ├── InfoPlist.xcstrings
│   │   │   │   ├── LearnMoreView.swift
│   │   │   │   ├── Localizable.xcstrings
│   │   │   │   └── ViewModel.swift
│   │   │   ├── Diorama.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── Dioramas.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── Packages
│   │   │   │   └── RealityKitContent
│   │   │   │       ├── Package.realitycomposerpro
│   │   │   │       │   ├── Library
│   │   │   │       │   ├── PluginData
│   │   │   │       │   ├── ProjectData
│   │   │   │       │   │   └── main.json
│   │   │   │       │   └── WorkspaceData
│   │   │   │       │       ├── SceneMetadataList.json
│   │   │   │       │       └── Settings.rcprojectdata
│   │   │   │       ├── Sources
│   │   │   │       │   └── RealityKitContent
│   │   │   │       │       ├── RealityKitContent.rkassets
│   │   │   │       │       │   ├── CatalinaData
│   │   │   │       │       │   │   ├── DioramaCatalina_ao.png
│   │   │   │       │       │   │   ├── DioramaCatalina_bc.png
│   │   │   │       │       │   │   ├── DioramaCatalina_n.png
│   │   │   │       │       │   │   ├── DioramaCatalina_r.png
│   │   │   │       │       │   │   └── DioramaCatalina_refit_h.exr
│   │   │   │       │       │   ├── ParticleEmitterPresetTextures
│   │   │   │       │       │   │   └── dustsheet.exr
│   │   │   │       │       │   ├── TrailPath_Export
│   │   │   │       │       │   │   ├── 0
│   │   │   │       │       │   │   │   ├── Catalina_TrailA.usdz
│   │   │   │       │       │   │   │   ├── Catalina_TrailB.usdz
│   │   │   │       │       │   │   │   ├── Yosemite_TrailA.usdz
│   │   │   │       │       │   │   │   ├── Yosemite_TrailB.usdz
│   │   │   │       │       │   │   │   └── hilight_gradient.png
│   │   │   │       │       │   │   └── TrailPath_Export.usdc
│   │   │   │       │       │   ├── YosemiteData
│   │   │   │       │       │   │   ├── DioramaYosemite_ao.png
│   │   │   │       │       │   │   ├── DioramaYosemite_bc.png
│   │   │   │       │       │   │   ├── DioramaYosemite_n.png
│   │   │   │       │       │   │   ├── DioramaYosemite_r.png
│   │   │   │       │       │   │   └── DioramaYosemite_refit_h.exr
│   │   │   │       │       │   ├── Bird.usdz
│   │   │   │       │       │   ├── Bird_Call_1.wav
│   │   │   │       │       │   ├── Bird_Call_2.wav
│   │   │   │       │       │   ├── Bird_With_Audio.usda
│   │   │   │       │       │   ├── Catalina.usdz
│   │   │   │       │       │   ├── Cloud_A.usda
│   │   │   │       │       │   ├── Cloud_B.usda
│   │   │   │       │       │   ├── Cloud_C.usda
│   │   │   │       │       │   ├── Cloud_Chunk.usda
│   │   │   │       │       │   ├── DioramaAssembled.usda
│   │   │   │       │       │   ├── Diorama_Base.usdz
│   │   │   │       │       │   ├── FlatTerrain.usdz
│   │   │   │       │       │   ├── Forest_Sounds.wav
│   │   │   │       │       │   ├── Location_Pin.usdz
│   │   │   │       │       │   ├── Materials.usda
│   │   │   │       │       │   ├── Ocean_Sounds.wav
│   │   │   │       │       │   ├── SmoothConcrete.usdz
│   │   │   │       │       │   └── Yosemite.usdz
│   │   │   │       │       ├── BillboardComponent.swift
│   │   │   │       │       ├── BillboardSystem.swift
│   │   │   │       │       ├── PointOfInterestComponent.swift
│   │   │   │       │       ├── RealityKitContent.swift
│   │   │   │       │       ├── RegionSpecificComponent.swift
│   │   │   │       │       ├── ShaderGraphMaterials.swift
│   │   │   │       │       ├── Style.swift
│   │   │   │       │       ├── TrailAnimationSystem.swift
│   │   │   │       │       └── TrailComponent.swift
│   │   │   │       ├── Package.swift
│   │   │   │       └── README.md
│   │   │   ├── LICENSE.txt
│   │   │   ├── README.md
│   │   │   └── metadata.json
│   │   ├── enabling-video-reflections-in-an-immersive-environment
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── DestinationVideo
│   │   │   │   ├── Extensions
│   │   │   │   │   ├── AVExtensions.swift
│   │   │   │   │   ├── DestinationVideoExtensions.swift
│   │   │   │   │   └── MultiplatformExtensions.swift
│   │   │   │   ├── Model
│   │   │   │   │   ├── Data
│   │   │   │   │   │   ├── Genre.swift
│   │   │   │   │   │   ├── Importer.swift
│   │   │   │   │   │   ├── Person.swift
│   │   │   │   │   │   ├── PreviewData.swift
│   │   │   │   │   │   ├── RelationshipMapping.swift
│   │   │   │   │   │   ├── SampleData.swift
│   │   │   │   │   │   ├── UpNextItem.swift
│   │   │   │   │   │   └── Video.swift
│   │   │   │   │   ├── visionOS
│   │   │   │   │   │   ├── EnvironmentStateHandler.swift
│   │   │   │   │   │   └── ImmersiveEnvironment.swift
│   │   │   │   │   ├── Category.swift
│   │   │   │   │   ├── Constants.swift
│   │   │   │   │   ├── NavigationNode.swift
│   │   │   │   │   └── Tabs.swift
│   │   │   │   ├── Player
│   │   │   │   │   ├── InlinePlayerView.swift
│   │   │   │   │   ├── PlayerModel.swift
│   │   │   │   │   ├── PlayerView.swift
│   │   │   │   │   ├── SystemPlayerView.swift
│   │   │   │   │   └── UpNextView.swift
│   │   │   │   ├── Preview Content
│   │   │   │   │   └── Preview Assets.xcassets
│   │   │   │   │       └── Contents.json
│   │   │   │   ├── Resources
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AccentColor.colorset
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── AppIcon.appiconset
│   │   │   │   │   │   │   ├── AppIcon.png
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   ├── DarkAppIcon.png
│   │   │   │   │   │   │   ├── TintableAppIcon.png
│   │   │   │   │   │   │   ├── icon_128x128.png
│   │   │   │   │   │   │   ├── icon_128x128@2x.png
│   │   │   │   │   │   │   ├── icon_16x16.png
│   │   │   │   │   │   │   ├── icon_16x16@2x.png
│   │   │   │   │   │   │   ├── icon_256x256.png
│   │   │   │   │   │   │   ├── icon_256x256@2x.png
│   │   │   │   │   │   │   ├── icon_32x32.png
│   │   │   │   │   │   │   ├── icon_32x32@2x.png
│   │   │   │   │   │   │   ├── icon_512x512.png
│   │   │   │   │   │   │   └── icon_512x512@2x.png
│   │   │   │   │   │   ├── AppIcon.brandassets
│   │   │   │   │   │   │   ├── App Icon - App Store.imagestack
│   │   │   │   │   │   │   │   ├── Back.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   ├── Front.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   ├── Middle.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── App Icon.imagestack
│   │   │   │   │   │   │   │   ├── Back.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   ├── Back.png
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   ├── Front.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   │   │   └── Front.png
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   ├── Middle.imagestacklayer
│   │   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Top Shelf Image Wide.imageset
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Top Shelf Image.imageset
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   ├── Back.png
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   │   └── Front.png
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── BOT-anist_landscape.imageset
│   │   │   │   │   │   │   ├── BOT-anist_landscape.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── BOT-anist_portrait.imageset
│   │   │   │   │   │   │   ├── BOT-anist_portrait.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── amazing_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── amazing-animation-poster.png
│   │   │   │   │   │   ├── animals_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── cute-animals-poster.png
│   │   │   │   │   │   ├── beach_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── beach_landscape.png
│   │   │   │   │   │   ├── beach_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── beach_portrait.png
│   │   │   │   │   │   ├── camping_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── camping_landscape.png
│   │   │   │   │   │   ├── camping_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── camping_portrait.png
│   │   │   │   │   │   ├── cinematic_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── cinematic_poster.png
│   │   │   │   │   │   ├── creek_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── creek_landscape.png
│   │   │   │   │   │   ├── creek_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── creek_portrait.png
│   │   │   │   │   │   ├── dance_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── dance_landscape.png
│   │   │   │   │   │   ├── dance_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── dance_portrait.png
│   │   │   │   │   │   ├── discovery_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── discovery_landscape.png
│   │   │   │   │   │   ├── discovery_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── discovery_portrait.png
│   │   │   │   │   │   ├── dv_logo.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── dv_logo@2x.png
│   │   │   │   │   │   ├── extraordinary_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── extraordinary-poster.png
│   │   │   │   │   │   ├── forest_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── forest_poster.png
│   │   │   │   │   │   ├── hillside_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── hillside_landscape.png
│   │   │   │   │   │   ├── hillside_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── hillside_portrait.png
│   │   │   │   │   │   ├── lab_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── lab_landscape.png
│   │   │   │   │   │   ├── lab_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── lab_portrait.png
│   │   │   │   │   │   ├── lake_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── lake_landscape.png
│   │   │   │   │   │   ├── lake_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── lake_portrait.png
│   │   │   │   │   │   ├── landing_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── landing_landscape.png
│   │   │   │   │   │   ├── landing_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── landing_portriat.png
│   │   │   │   │   │   ├── ocean_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── ocean_landscape.png
│   │   │   │   │   │   ├── ocean_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── ocean_portrait.png
│   │   │   │   │   │   ├── park_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── park_landscape.png
│   │   │   │   │   │   ├── park_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── park_portrait.png
│   │   │   │   │   │   ├── samples_landscape.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── samples_landscape.png
│   │   │   │   │   │   ├── samples_portrait.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── samples_portriat.png
│   │   │   │   │   │   ├── sea_poster.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── by-the-sea-poster.png
│   │   │   │   │   │   ├── studio_thumbnail_dark.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── studio_thumbnail_dark.png
│   │   │   │   │   │   ├── studio_thumbnail_light.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── studio_thumbnail_light.png
│   │   │   │   │   │   ├── tvBackground.colorset
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Videos
│   │   │   │   │   │   ├── BOT-anist_video.mov
│   │   │   │   │   │   └── dance_video.mov
│   │   │   │   │   ├── de.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── fr.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── hi.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── ja.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── ko.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   ├── zh_CN.lproj
│   │   │   │   │   │   └── InfoPlist.strings
│   │   │   │   │   └── Localizable.xcstrings
│   │   │   │   ├── SharePlay
│   │   │   │   │   ├── WatchingActivity.swift
│   │   │   │   │   └── WatchingCoordinator.swift
│   │   │   │   ├── Views
│   │   │   │   │   ├── visionOS
│   │   │   │   │   │   ├── ImmersiveEnvironmentPickerView.swift
│   │   │   │   │   │   ├── ImmersiveEnvironmentView.swift
│   │   │   │   │   │   ├── ProfileButton.swift
│   │   │   │   │   │   └── TrailerView.swift
│   │   │   │   │   ├── ButtonStyle.swift
│   │   │   │   │   ├── CategoryListView.swift
│   │   │   │   │   ├── CategoryView.swift
│   │   │   │   │   ├── DetailView.swift
│   │   │   │   │   ├── GradientView.swift
│   │   │   │   │   ├── HeroView.swift
│   │   │   │   │   ├── LibraryView.swift
│   │   │   │   │   ├── VideoCardView.swift
│   │   │   │   │   ├── VideoInfoView.swift
│   │   │   │   │   ├── VideoListView.swift
│   │   │   │   │   ├── ViewModifiers.swift
│   │   │   │   │   └── WatchNowView.swift
│   │   │   │   ├── ContentView.swift
│   │   │   │   ├── DestinationTabs.swift
│   │   │   │   ├── DestinationVideo.entitlements
│   │   │   │   ├── DestinationVideo.swift
│   │   │   │   ├── Info.plist
│   │   │   │   └── PlayerWindow.swift
│   │   │   ├── DestinationVideo.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── Packages
│   │   │   │   └── Studio
│   │   │   │       ├── Package.realitycomposerpro
│   │   │   │       │   ├── ProjectData
│   │   │   │       │   │   └── main.json
│   │   │   │       │   └── WorkspaceData
│   │   │   │       │       ├── SceneMetadataList.json
│   │   │   │       │       └── Settings.rcprojectdata
│   │   │   │       ├── Sources
│   │   │   │       │   └── Studio
│   │   │   │       │       ├── Studio.rkassets
│   │   │   │       │       │   ├── ibl
│   │   │   │       │       │   │   ├── Studio_IBL_LatLong_Dark.exr
│   │   │   │       │       │   │   └── Studio_IBL_LatLong_Light.exr
│   │   │   │       │       │   ├── meshes
│   │   │   │       │       │   │   ├── Studio.usdc
│   │   │   │       │       │   │   ├── Studio_floor_2_2_Lightspill.usdc
│   │   │   │       │       │   │   ├── Studio_floor_2_Lightspill.usdc
│   │   │   │       │       │   │   └── dome.usdc
│   │   │   │       │       │   ├── scenes
│   │   │   │       │       │   │   ├── Common.usda
│   │   │   │       │       │   │   ├── Floor.usda
│   │   │   │       │       │   │   ├── StudioDark.usda
│   │   │   │       │       │   │   └── StudioLight.usda
│   │   │   │       │       │   ├── textures
│   │   │   │       │       │   │   ├── common
│   │   │   │       │       │   │   │   └── DefaultAttenuationMap.exr
│   │   │   │       │       │   │   ├── dark
│   │   │   │       │       │   │   │   ├── BakingGroup1_1_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup1_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup2_2_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup2_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup3_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup4_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup5_d.png
│   │   │   │       │       │   │   │   ├── BakingGroup6_d.png
│   │   │   │       │       │   │   │   └── BakingGroup7_d.png
│   │   │   │       │       │   │   ├── light
│   │   │   │       │       │   │   │   ├── BakingGroup1.png
│   │   │   │       │       │   │   │   ├── BakingGroup1_1.png
│   │   │   │       │       │   │   │   ├── BakingGroup2.png
│   │   │   │       │       │   │   │   ├── BakingGroup2_2.png
│   │   │   │       │       │   │   │   ├── BakingGroup3.png
│   │   │   │       │       │   │   │   ├── BakingGroup4.png
│   │   │   │       │       │   │   │   ├── BakingGroup5.png
│   │   │   │       │       │   │   │   ├── BakingGroup6.png
│   │   │   │       │       │   │   │   └── BakingGroup7.png
│   │   │   │       │       │   │   └── skies
│   │   │   │       │       │   │       ├── Studio_sky_LatLong_Dark.exr
│   │   │   │       │       │   │       └── Studio_sky_LatLong_Light.exr
│   │   │   │       │       │   └── AAA_MainScene.usda
│   │   │   │       │       └── Studio.swift
│   │   │   │       └── Package.swift
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── exploring-object-tracking-with-arkit
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── ObjectTracking
│   │   │   │   ├── App
│   │   │   │   │   ├── AppState.swift
│   │   │   │   │   ├── ObjectAnchorVisualization.swift
│   │   │   │   │   └── ReferenceObjectLoader.swift
│   │   │   │   ├── Extensions
│   │   │   │   │   └── Entity+ObjectTracking.swift
│   │   │   │   ├── Views
│   │   │   │   │   ├── HomeView.swift
│   │   │   │   │   ├── InfoLabel.swift
│   │   │   │   │   ├── ListEntryView.swift
│   │   │   │   │   └── ObjectTrackingRealityView.swift
│   │   │   │   ├── Info.plist
│   │   │   │   └── ObjectTrackingApp.swift
│   │   │   ├── ObjectTracking.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── ObjectTracking.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── Reference Objects
│   │   │   │   └── Apple_Magic_Keyboard.referenceobject
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── happy-beam
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── HappyBeam
│   │   │   │   ├── Assets.xcassets
│   │   │   │   │   ├── AccentColor.colorset
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   ├── Bottom Layer@2x.png
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   └── topLayer@2x.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── finish-clouds.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── finish-clouds.png
│   │   │   │   │   ├── gesture_hand.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── gesture_hand.svg
│   │   │   │   │   ├── greatJob.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── greatJob@2x.png
│   │   │   │   │   ├── hands-diagram.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── hands-diagram.png
│   │   │   │   │   ├── keyboardGameController.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── keyboardGameController.svg
│   │   │   │   │   ├── shareplayGraphic.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── shareplayGraphic@2x.png
│   │   │   │   │   ├── splashScreen.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── splashScreenGraphic@2x.png
│   │   │   │   │   └── Contents.json
│   │   │   │   ├── Gameplay
│   │   │   │   │   ├── BeamCollisions.swift
│   │   │   │   │   ├── Clouds.swift
│   │   │   │   │   ├── HeartGestureModel.swift
│   │   │   │   │   ├── Multiplayer.swift
│   │   │   │   │   └── Players.swift
│   │   │   │   ├── Preview Content
│   │   │   │   │   └── Preview Assets.xcassets
│   │   │   │   │       └── Contents.json
│   │   │   │   ├── Sounds
│   │   │   │   │   ├── cloudHit1.m4a
│   │   │   │   │   ├── cloudHit2.m4a
│   │   │   │   │   ├── cloudHit3.m4a
│   │   │   │   │   ├── cloudHit4.m4a
│   │   │   │   │   ├── happyBeamGameplay.m4a
│   │   │   │   │   ├── happyBeamMenu.m4a
│   │   │   │   │   └── happyBeamVictory.m4a
│   │   │   │   ├── USDZs
│   │   │   │   │   ├── UpdatedGrumpyScene2.usdz
│   │   │   │   │   ├── cloud.usdz
│   │   │   │   │   └── fireworks.usdz
│   │   │   │   ├── Views
│   │   │   │   │   ├── HappyBeam.swift
│   │   │   │   │   ├── Lobby.swift
│   │   │   │   │   ├── MultiPlay.swift
│   │   │   │   │   ├── MultiScore.swift
│   │   │   │   │   ├── SoloPlay.swift
│   │   │   │   │   ├── SoloScore.swift
│   │   │   │   │   └── Start.swift
│   │   │   │   ├── Extensions.swift
│   │   │   │   ├── GameModel.swift
│   │   │   │   ├── GlobalEntities.swift
│   │   │   │   ├── HappyBeam.entitlements
│   │   │   │   ├── HappyBeamApp.swift
│   │   │   │   ├── HappyBeamSpace.swift
│   │   │   │   ├── Info.plist
│   │   │   │   ├── InfoPlist.xcstrings
│   │   │   │   └── Localizable.xcstrings
│   │   │   ├── HappyBeam.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── HappyBeam.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── Packages
│   │   │   │   └── HappyBeamAssets
│   │   │   │       ├── Package.realitycomposerpro
│   │   │   │       │   ├── ProjectData
│   │   │   │       │   │   └── main.json
│   │   │   │       │   └── WorkspaceData
│   │   │   │       │       ├── SceneMetadataList.json
│   │   │   │       │       └── Settings.rcprojectdata
│   │   │   │       ├── Sources
│   │   │   │       │   └── HappyBeamAssets
│   │   │   │       │       ├── HappyBeamAssets.rkassets
│   │   │   │       │       │   ├── UpdatedGrumpyScene2
│   │   │   │       │       │   │   ├── 0
│   │   │   │       │       │   │   │   ├── M_cloud_body_baseColor.jpg
│   │   │   │       │       │   │   │   ├── M_cloud_body_emmissive.jpg
│   │   │   │       │       │   │   │   ├── M_cloud_body_normal.png
│   │   │   │       │       │   │   │   ├── M_cloud_body_occlusion.jpg
│   │   │   │       │       │   │   │   ├── M_cloud_body_roughness.jpg
│   │   │   │       │       │   │   │   ├── M_cloud_face_baseColor.jpg
│   │   │   │       │       │   │   │   ├── cloud_002_anim.usdz
│   │   │   │       │       │   │   │   ├── happyClouds_baseColor_1.png
│   │   │   │       │       │   │   │   ├── m_happyCloud_face_normal_1.png
│   │   │   │       │       │   │   │   └── m_happyCloud_face_roughness_1.jpg
│   │   │   │       │       │   │   ├── UpdatedGrumpyScene2.usdc
│   │   │   │       │       │   │   └── cloud_lod1_anim_001_2-10.usdc
│   │   │   │       │       │   ├── textures
│   │   │   │       │       │   │   ├── heartBeam_basecolor_1.png
│   │   │   │       │       │   │   ├── heartBeam_metallic_1.jpg
│   │   │   │       │       │   │   ├── heartBeam_normal_1.png
│   │   │   │       │       │   │   ├── heartBeam_roughness_1.jpg
│   │   │   │       │       │   │   ├── heartLight_M_heartLight_baseColor 1.png
│   │   │   │       │       │   │   ├── heartLight_M_heartLight_baseColor.png
│   │   │   │       │       │   │   ├── heartLight_M_heartLight_metallic 1.jpg
│   │   │   │       │       │   │   ├── heartLight_M_heartLight_metallic.jpg
│   │   │   │       │       │   │   ├── heartLight_M_heartLight_normal 1.png
│   │   │   │       │       │   │   ├── heartLight_M_heartLight_normal.png
│   │   │   │       │       │   │   ├── heartLight_M_heartLight_roughness 1.jpg
│   │   │   │       │       │   │   ├── heartLight_M_heartLight_roughness.jpg
│   │   │   │       │       │   │   ├── mat_heart_Base_color_1.png
│   │   │   │       │       │   │   ├── mat_heart_Metallic_1.png
│   │   │   │       │       │   │   ├── mat_heart_Normal_1.png
│   │   │   │       │       │   │   └── mat_heart_Roughness_1.png
│   │   │   │       │       │   ├── Cloud.usda
│   │   │   │       │       │   ├── Heart.usda
│   │   │   │       │       │   ├── HeartBeam.usd
│   │   │   │       │       │   ├── HeartBlaster.usda
│   │   │   │       │       │   ├── HeartTurret.usda
│   │   │   │       │       │   ├── M_heartTurret_baseColor_1.png
│   │   │   │       │       │   ├── M_heartTurret_metallic_1.jpg
│   │   │   │       │       │   ├── M_heartTurret_normal_1.png
│   │   │   │       │       │   ├── M_heartTurret_roughness_1.jpg
│   │   │   │       │       │   ├── UpdatedGrumpyScene2.usdz
│   │   │   │       │       │   ├── heartBeam_basecolor_1.png
│   │   │   │       │       │   ├── heartBeam_metallic_1.jpg
│   │   │   │       │       │   ├── heartBeam_normal_1.png
│   │   │   │       │       │   ├── heartBeam_opacity2_1.png
│   │   │   │       │       │   ├── heartLight_M_heartLight_baseColor.png
│   │   │   │       │       │   ├── heartLight_M_heartLight_emissive.jpg
│   │   │   │       │       │   ├── heartLight_M_heartLight_metallic.jpg
│   │   │   │       │       │   ├── heartLight_M_heartLight_normal.png
│   │   │   │       │       │   ├── heartLight_M_heartLight_roughness.jpg
│   │   │   │       │       │   ├── heartLight_longer.usdc
│   │   │   │       │       │   ├── heartTurret.usdc
│   │   │   │       │       │   ├── heart_new.usdc
│   │   │   │       │       │   ├── mat_heart_Base_color_1.png
│   │   │   │       │       │   ├── mat_heart_Metallic_1.png
│   │   │   │       │       │   ├── mat_heart_Mixed_AO_1.png
│   │   │   │       │       │   ├── mat_heart_Normal_1.png
│   │   │   │       │       │   ├── mat_heart_Roughness_1.png
│   │   │   │       │       │   └── new_heart_ramp.png
│   │   │   │       │       └── HappyBeamAssets.swift
│   │   │   │       ├── Package.swift
│   │   │   │       └── README.md
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── hello-world
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── Packages
│   │   │   │   └── WorldAssets
│   │   │   │       ├── Package.realitycomposerpro
│   │   │   │       │   └── ProjectData
│   │   │   │       │       └── main.json
│   │   │   │       ├── Sources
│   │   │   │       │   └── WorldAssets
│   │   │   │       │       ├── WorldAssets.rkassets
│   │   │   │       │       │   ├── Moon
│   │   │   │       │       │   │   ├── 0
│   │   │   │       │       │   │   │   ├── M_moon_baseColor_1.jpg
│   │   │   │       │       │   │   │   ├── M_moon_emissive_1.jpg
│   │   │   │       │       │   │   │   ├── M_moon_metallic_1.jpg
│   │   │   │       │       │   │   │   ├── M_moon_normal_1.jpg
│   │   │   │       │       │   │   │   ├── M_moon_occlusion_1.jpg
│   │   │   │       │       │   │   │   └── M_moon_roughness_2.jpg
│   │   │   │       │       │   │   ├── M_earth_baseColor_combined.jpg
│   │   │   │       │       │   │   └── Moon.exported_compressed.usdc
│   │   │   │       │       │   ├── Pole
│   │   │   │       │       │   │   ├── 0
│   │   │   │       │       │   │   │   ├── M_arrow_baseColor_1.png
│   │   │   │       │       │   │   │   ├── M_arrow_emissive_1.jpg
│   │   │   │       │       │   │   │   ├── M_arrow_metallic_1.jpg
│   │   │   │       │       │   │   │   ├── M_arrow_normal_1.jpg
│   │   │   │       │       │   │   │   ├── M_arrow_roughness_1.jpg
│   │   │   │       │       │   │   │   └── arrow_opacity_1.png
│   │   │   │       │       │   │   └── Pole.exported_compressed.usdc
│   │   │   │       │       │   ├── Satellite
│   │   │   │       │       │   │   ├── 0
│   │   │   │       │       │   │   │   ├── M_satellite_baseColor_1.jpg
│   │   │   │       │       │   │   │   ├── M_satellite_metallic_1.jpg
│   │   │   │       │       │   │   │   ├── M_satellite_normal_1.jpg
│   │   │   │       │       │   │   │   ├── M_satellite_occlusion_1.jpg
│   │   │   │       │       │   │   │   └── M_satellite_roughness_1.jpg
│   │   │   │       │       │   │   └── Satellite.exported_compressed.usdc
│   │   │   │       │       │   ├── Sun
│   │   │   │       │       │   │   ├── 0
│   │   │   │       │       │   │   │   ├── M_sun_baseColor_1.jpg
│   │   │   │       │       │   │   │   ├── M_sun_emissive_2.jpg
│   │   │   │       │       │   │   │   ├── M_sun_metallic_1.jpg
│   │   │   │       │       │   │   │   ├── M_sun_normal_1.jpg
│   │   │   │       │       │   │   │   ├── M_sun_occlusion_1.jpg
│   │   │   │       │       │   │   │   └── M_sun_roughness_1.jpg
│   │   │   │       │       │   │   └── Sun.exported_compressed.usdc
│   │   │   │       │       │   ├── Telescope
│   │   │   │       │       │   │   ├── 0
│   │   │   │       │       │   │   │   ├── M_telescopeBase_baseColor_1.jpg
│   │   │   │       │       │   │   │   ├── M_telescopeBase_emissive_1.jpg
│   │   │   │       │       │   │   │   ├── M_telescopeBase_metallic_1.jpg
│   │   │   │       │       │   │   │   ├── M_telescopeBase_normal_1.jpg
│   │   │   │       │       │   │   │   ├── M_telescopeBase_occlusion_1.jpg
│   │   │   │       │       │   │   │   ├── M_telescopeBase_roughness_1.jpg
│   │   │   │       │       │   │   │   ├── M_telescopeReflectors_baseColor_1.png
│   │   │   │       │       │   │   │   ├── M_telescopeReflectors_emissive_1.jpg
│   │   │   │       │       │   │   │   ├── M_telescopeReflectors_metallic_1.jpg
│   │   │   │       │       │   │   │   ├── M_telescopeReflectors_normal_1.jpg
│   │   │   │       │       │   │   │   ├── M_telescopeReflectors_occlusion_1.jpg
│   │   │   │       │       │   │   │   └── M_telescopeReflectors_roughness_1.jpg
│   │   │   │       │       │   │   └── Telescope.exported_compressed.usdc
│   │   │   │       │       │   ├── Earth.usda
│   │   │   │       │       │   ├── Globe.usda
│   │   │   │       │       │   ├── Globe.usdz
│   │   │   │       │       │   ├── M_earth_baseColor.png
│   │   │   │       │       │   ├── M_earth_clouds_normal.png
│   │   │   │       │       │   ├── M_earth_emissive.jpg
│   │   │   │       │       │   ├── M_earth_normal.png
│   │   │   │       │       │   ├── M_earth_roughness.jpg
│   │   │   │       │       │   ├── Moon.usda
│   │   │   │       │       │   ├── Pole.usda
│   │   │   │       │       │   ├── Pole.usdc
│   │   │   │       │       │   ├── Satellite.usda
│   │   │   │       │       │   ├── Sun.usda
│   │   │   │       │       │   ├── Telescope.usda
│   │   │   │       │       │   ├── earthClouds_opacity.png
│   │   │   │       │       │   ├── earth_004_clouds_resized.usdc
│   │   │   │       │       │   └── earth_sphere_equirectangular.usdc
│   │   │   │       │       ├── SunPositionSystem.swift
│   │   │   │       │       └── WorldAssets.swift
│   │   │   │       ├── Package.swift
│   │   │   │       └── README.md
│   │   │   ├── World
│   │   │   │   ├── Entities
│   │   │   │   │   ├── EarthEntity+Configuration.swift
│   │   │   │   │   ├── EarthEntity.swift
│   │   │   │   │   ├── Entity+Sunlight.swift
│   │   │   │   │   ├── Entity+Trace.swift
│   │   │   │   │   ├── SatelliteEntity+Configuration.swift
│   │   │   │   │   └── SatelliteEntity.swift
│   │   │   │   ├── Globe
│   │   │   │   │   ├── Globe.swift
│   │   │   │   │   ├── GlobeControls.swift
│   │   │   │   │   ├── GlobeModule.swift
│   │   │   │   │   └── GlobeToggle.swift
│   │   │   │   ├── Model
│   │   │   │   │   ├── Module.swift
│   │   │   │   │   └── ViewModel.swift
│   │   │   │   ├── Modifiers
│   │   │   │   │   ├── DragRotationModifier.swift
│   │   │   │   │   ├── PlacementGesturesModifier.swift
│   │   │   │   │   └── TypeTextModifier.swift
│   │   │   │   ├── Modules
│   │   │   │   │   ├── ModuleCard.swift
│   │   │   │   │   ├── ModuleDetail.swift
│   │   │   │   │   ├── Modules.swift
│   │   │   │   │   └── TableOfContents.swift
│   │   │   │   ├── Orbit
│   │   │   │   │   ├── Orbit.swift
│   │   │   │   │   ├── OrbitModule.swift
│   │   │   │   │   └── OrbitToggle.swift
│   │   │   │   ├── Packages
│   │   │   │   │   └── WorldAssets
│   │   │   │   ├── Preview Content
│   │   │   │   │   └── Preview Assets.xcassets
│   │   │   │   │       └── Contents.json
│   │   │   │   ├── RealityViews
│   │   │   │   │   ├── Earth.swift
│   │   │   │   │   ├── Starfield.swift
│   │   │   │   │   └── Sun.swift
│   │   │   │   ├── Resources
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AccentColor.colorset
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   ├── Back.png
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   │   └── Front.png
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── EarthHalf.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── EarthHalf@2x.png
│   │   │   │   │   │   ├── GlobeHero.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── GlobeHero@2x.png
│   │   │   │   │   │   ├── SolarBackground.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── SolarBackground@2x.png
│   │   │   │   │   │   ├── SolarHero.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── SolarHero@2x.png
│   │   │   │   │   │   ├── Starfield.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── Starfield.jpg
│   │   │   │   │   │   ├── SunSliver.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── SunSliver@2x.png
│   │   │   │   │   │   ├── TrailGradient.imageset
│   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   └── TrailGradient.jpg
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   └── Sunlight.skybox
│   │   │   │   │       └── Sunlight.png
│   │   │   │   ├── Settings
│   │   │   │   │   ├── EarthSettings.swift
│   │   │   │   │   ├── GlobeSettings.swift
│   │   │   │   │   ├── OrbitSettings.swift
│   │   │   │   │   ├── SatelliteSettings.swift
│   │   │   │   │   ├── SettingsButton.swift
│   │   │   │   │   ├── SliderGridRow.swift
│   │   │   │   │   └── SolarSystemSettings.swift
│   │   │   │   ├── Solar System
│   │   │   │   │   ├── SolarSystem.swift
│   │   │   │   │   ├── SolarSystemControls.swift
│   │   │   │   │   ├── SolarSystemModule.swift
│   │   │   │   │   └── SolarSystemToggle.swift
│   │   │   │   ├── Systems
│   │   │   │   │   ├── RotationSystem.swift
│   │   │   │   │   └── TraceSystem.swift
│   │   │   │   ├── Info.plist
│   │   │   │   ├── InfoPlist.xcstrings
│   │   │   │   ├── Localizable.xcstrings
│   │   │   │   └── WorldApp.swift
│   │   │   ├── World.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── World.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   ├── README.md
│   │   │   └── metadata.json
│   │   ├── incorporating-real-world-surroundings-in-an-immersive-experience
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── SceneReconstructionExample
│   │   │   │   ├── ContentView.swift
│   │   │   │   ├── CubeMeshInteraction.swift
│   │   │   │   ├── EntityModel.swift
│   │   │   │   ├── Extensions.swift
│   │   │   │   ├── Info.plist
│   │   │   │   └── SceneReconstructionExampleApp.swift
│   │   │   ├── SceneReconstructionExample.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       ├── xcschemes
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   ├── placing-content-on-detected-planes
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── ObjectPlacement
│   │   │   │   ├── 3D Models
│   │   │   │   │   ├── Box.usdz
│   │   │   │   │   ├── Cone.usdz
│   │   │   │   │   ├── Cube.usdz
│   │   │   │   │   └── Cylinder.usdz
│   │   │   │   ├── App
│   │   │   │   │   ├── AppState.swift
│   │   │   │   │   ├── DragState.swift
│   │   │   │   │   ├── PlaceableObject.swift
│   │   │   │   │   ├── PlacementManager.swift
│   │   │   │   │   └── PlacementState.swift
│   │   │   │   ├── Utilities
│   │   │   │   │   ├── GeometryUtilities.swift
│   │   │   │   │   ├── ModelLoader.swift
│   │   │   │   │   ├── PersistenceManager.swift
│   │   │   │   │   ├── PlaneAnchorHandler.swift
│   │   │   │   │   └── PlaneProjector.swift
│   │   │   │   ├── Views
│   │   │   │   │   ├── DeleteButton.swift
│   │   │   │   │   ├── HomeView.swift
│   │   │   │   │   ├── InfoLabel.swift
│   │   │   │   │   ├── ObjectPlacementMenuView.swift
│   │   │   │   │   ├── ObjectPlacementRealityView.swift
│   │   │   │   │   ├── ObjectSelectionView.swift
│   │   │   │   │   ├── PlacementTooltip.swift
│   │   │   │   │   └── TooltipView.swift
│   │   │   │   ├── Info.plist
│   │   │   │   └── ObjectPlacementApp.swift
│   │   │   ├── ObjectPlacement.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       ├── xcschemes
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── ObjectPlacement.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   ├── README.md
│   │   │   └── metadata.json
│   │   ├── playing-spatial-audio
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── SpatialAudio
│   │   │   │   ├── App
│   │   │   │   │   ├── Assets.xcassets
│   │   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── Preview Assets.xcassets
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── EntryPoint.swift
│   │   │   │   │   └── Info.plist
│   │   │   │   ├── Resources
│   │   │   │   │   └── FunkySynth.m4a
│   │   │   │   ├── Views
│   │   │   │   │   ├── DecibelSlider.swift
│   │   │   │   │   └── SpatialAudioView.swift
│   │   │   │   └── Visualizer
│   │   │   │       └── AxisVisualizer.swift
│   │   │   ├── SpatialAudio.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   ├── README.md
│   │   │   └── metadata.json
│   │   ├── progressive
│   │   │   └── project.zip
│   │   ├── realitykit
│   │   │   └── project.zip
│   │   ├── swift-splash
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── Packages
│   │   │   │   └── SwiftSplashTrackPieces
│   │   │   │       ├── Package.realitycomposerpro
│   │   │   │       │   ├── ProjectData
│   │   │   │       │   │   └── main.json
│   │   │   │       │   └── WorkspaceData
│   │   │   │       │       ├── SceneMetadataList.json
│   │   │   │       │       ├── Settings.rcprojectdata
│   │   │   │       │       └── amandaestrada.rcuserdata
│   │   │   │       ├── Sources
│   │   │   │       │   └── SwiftSplashTrackPieces
│   │   │   │       │       ├── Components
│   │   │   │       │       │   ├── Connectable.swift
│   │   │   │       │       │   ├── ConnectableStateComponent.swift
│   │   │   │       │       │   └── MarkerComponents.swift
│   │   │   │       │       ├── Extensions
│   │   │   │       │       │   ├── Entity+Utilities.swift
│   │   │   │       │       │   ├── Float+Utilities.swift
│   │   │   │       │       │   └── SIMD+Utilities.swift
│   │   │   │       │       ├── SwiftSplashTrackPieces.rkassets
│   │   │   │       │       │   ├── Fish
│   │   │   │       │       │   │   ├── Textures
│   │   │   │       │       │   │   │   ├── mat_fishAccessories_BaseColor.png
│   │   │   │       │       │   │   │   ├── mat_fishAccessories_Normal.png
│   │   │   │       │       │   │   │   ├── mat_fishAccessories_OcclusionRoughnessMetallic.png
│   │   │   │       │       │   │   │   ├── mat_fishAccessories_Roughness.png
│   │   │   │       │       │   │   │   ├── mat_fishBody_BaseColor.png
│   │   │   │       │       │   │   │   ├── mat_fishBody_Normal.png
│   │   │   │       │       │   │   │   ├── mat_fishBody_OcclusionRoughnessMetallic.png
│   │   │   │       │       │   │   │   ├── mat_fishBody_Roughness.png
│   │   │   │       │       │   │   │   ├── mat_fishEyes_BaseColor.png
│   │   │   │       │       │   │   │   ├── mat_fishEyes_Normal.png
│   │   │   │       │       │   │   │   ├── mat_fishEyes_OcclusionRoughnessMetallic.png
│   │   │   │       │       │   │   │   ├── mat_fishGlass_BaseColor.png
│   │   │   │       │       │   │   │   ├── mat_fishGlass_Normal.png
│   │   │   │       │       │   │   │   └── mat_fishGlass_OcclusionRoughnessMetallic.png
│   │   │   │       │       │   │   ├── animations
│   │   │   │       │       │   │   │   └── adventureFish_swim_slide01_anim.usdz
│   │   │   │       │       │   │   ├── adventureFish_idle_001_anim.usdz
│   │   │   │       │       │   │   └── adventureFish_swim_001_anim.usdz
│   │   │   │       │       │   ├── Goal
│   │   │   │       │       │   │   ├── Fish
│   │   │   │       │       │   │   │   ├── adventureFish_end_glass_idle_animation.usdz
│   │   │   │       │       │   │   │   ├── adventureFish_end_glass_ride_animation.usdz
│   │   │   │       │       │   │   │   ├── adventureFish_end_noGlass_idle_animation.usdz
│   │   │   │       │       │   │   │   └── adventureFish_end_noGlass_ride_animation.usdz
│   │   │   │       │       │   │   ├── end.usdz
│   │   │   │       │       │   │   ├── end_flag_glow.usd
│   │   │   │       │       │   │   ├── end_glow.usd
│   │   │   │       │       │   │   ├── end_water.usd
│   │   │   │       │       │   │   ├── flag_idle_animation.usdz
│   │   │   │       │       │   │   ├── flag_still_geo.usdz
│   │   │   │       │       │   │   ├── slideEnd_bottom.usdz
│   │   │   │       │       │   │   ├── slideEnd_top.usd
│   │   │   │       │       │   │   ├── slideEnd_top_glow.usd
│   │   │   │       │       │   │   ├── slide_end_water.usdz
│   │   │   │       │       │   │   └── waterFallSplash.usdz
│   │   │   │       │       │   ├── ParticleEmitterPresetTextures
│   │   │   │       │       │   │   ├── dustsheet.exr
│   │   │   │       │       │   │   ├── flare.exr
│   │   │   │       │       │   │   ├── flaresheet.exr
│   │   │   │       │       │   │   ├── halfRadial.png
│   │   │   │       │       │   │   ├── halfRadial1.png
│   │   │   │       │       │   │   ├── rain.png
│   │   │   │       │       │   │   ├── splashSpriteSheet.png
│   │   │   │       │       │   │   ├── testSplash.png
│   │   │   │       │       │   │   ├── twinkle.exr
│   │   │   │       │       │   │   └── waterDrop.png
│   │   │   │       │       │   ├── Slide_01
│   │   │   │       │       │   │   ├── Fish
│   │   │   │       │       │   │   │   ├── adventureFish_slide01_glass_ride_animation.usdz
│   │   │   │       │       │   │   │   └── adventureFish_slide01_noGlass_ride_animation.usdz
│   │   │   │       │       │   │   ├── slide01_bottom.usdz
│   │   │   │       │       │   │   ├── slide01_bottom_glow.usd
│   │   │   │       │       │   │   ├── slide01_top.usdz
│   │   │   │       │       │   │   ├── slide01_top_glow.usdz
│   │   │   │       │       │   │   ├── slide01_water.usdz
│   │   │   │       │       │   │   └── slide_01.usdz
│   │   │   │       │       │   ├── Slide_02
│   │   │   │       │       │   │   ├── Fish
│   │   │   │       │       │   │   │   ├── adventureFish_slide02_glass_ride_animation.usdz
│   │   │   │       │       │   │   │   └── adventureFish_slide02_noGlass_ride_animation.usdz
│   │   │   │       │       │   │   ├── slide02_bottom.usdz
│   │   │   │       │       │   │   ├── slide02_bottom_glow.usdz
│   │   │   │       │       │   │   ├── slide02_top.usdz
│   │   │   │       │       │   │   ├── slide02_top_glow.usd
│   │   │   │       │       │   │   └── slide02_water.usdz
│   │   │   │       │       │   ├── Slide_03
│   │   │   │       │       │   │   ├── Fish
│   │   │   │       │       │   │   │   ├── adventureFish_slide03_glass_ride_animation.usdz
│   │   │   │       │       │   │   │   └── adventureFish_slide03_noGlass_ride_animation.usdz
│   │   │   │       │       │   │   ├── slide03_bottom.usdz
│   │   │   │       │       │   │   ├── slide03_bottom_glow.usdz
│   │   │   │       │       │   │   ├── slide03_top.usdz
│   │   │   │       │       │   │   ├── slide03_top_glow.usdz
│   │   │   │       │       │   │   └── slide03_water.usdz
│   │   │   │       │       │   ├── Slide_04
│   │   │   │       │       │   │   ├── adventureFish_slide04_glass_ride_animation.usdz
│   │   │   │       │       │   │   ├── adventureFish_slide04_noGlass_ride_animation.usdz
│   │   │   │       │       │   │   ├── adventureFish_slide04_ride_animation.usdz
│   │   │   │       │       │   │   ├── slide04_bottom.usdz
│   │   │   │       │       │   │   ├── slide04_bottom_glow.usdz
│   │   │   │       │       │   │   ├── slide04_top.usdz
│   │   │   │       │       │   │   ├── slide04_top_glow.usdz
│   │   │   │       │       │   │   └── slide04_water.usdz
│   │   │   │       │       │   ├── Slide_05
│   │   │   │       │       │   │   ├── Fish
│   │   │   │       │       │   │   │   ├── adventureFish_slide05_glass_ride_animation.usdz
│   │   │   │       │       │   │   │   └── adventureFish_slide05_noGlass_ride_animation.usdz
│   │   │   │       │       │   │   ├── slide05_bottom.usdz
│   │   │   │       │       │   │   ├── slide05_bottom_glow.usdz
│   │   │   │       │       │   │   ├── slide05_top.usdz
│   │   │   │       │       │   │   ├── slide05_top_glow.usdz
│   │   │   │       │       │   │   └── slide05_water.usdz
│   │   │   │       │       │   ├── Start
│   │   │   │       │       │   │   ├── adventureFish_start_glass_idle_animation.usdz
│   │   │   │       │       │   │   ├── adventureFish_start_glass_ride_animation.usdz
│   │   │   │       │       │   │   ├── adventureFish_start_noGlass_idle_animation.usdz
│   │   │   │       │       │   │   ├── adventureFish_start_noGlass_ride_animation.usdz
│   │   │   │       │       │   │   ├── slideStart_bottom.usd
│   │   │   │       │       │   │   ├── slideStart_water.usdz
│   │   │   │       │       │   │   ├── start_glass.usd
│   │   │   │       │       │   │   ├── start_glow.usdz
│   │   │   │       │       │   │   ├── start_ride_animation.usdz
│   │   │   │       │       │   │   └── waterDrain_ride_animation.usdz
│   │   │   │       │       │   ├── Textures
│   │   │   │       │       │   │   ├── Metal
│   │   │   │       │       │   │   │   ├── mat_end_BaseColor_metal.png
│   │   │   │       │       │   │   │   ├── mat_end_Normal_metal.png
│   │   │   │       │       │   │   │   ├── mat_end_OcclusionRoughnessMetallic_metal.png
│   │   │   │       │       │   │   │   ├── mat_end_OcclusionRoughnessMetallic_plastic.png
│   │   │   │       │       │   │   │   ├── mat_slideTop_BaseColor_metal.png
│   │   │   │       │       │   │   │   ├── mat_slideTop_Emissive_metal.png
│   │   │   │       │       │   │   │   ├── mat_slideTop_Normal_metal.png
│   │   │   │       │       │   │   │   ├── mat_slideTop_OcclusionRoughnessMetallic_metal.png
│   │   │   │       │       │   │   │   ├── mat_slide_BaseColor_metal.png
│   │   │   │       │       │   │   │   ├── mat_slide_Normal_metal.png
│   │   │   │       │       │   │   │   ├── mat_slide_OcclusionRoughnessMetallic_metal.png
│   │   │   │       │       │   │   │   ├── mat_start_BaseColor_metal.png
│   │   │   │       │       │   │   │   ├── mat_start_Normal_metal.png
│   │   │   │       │       │   │   │   ├── mat_start_OcclusionRoughnessMetallic_metal.png
│   │   │   │       │       │   │   │   └── waterRidePieces_mat_slideTop_Opacity.png
│   │   │   │       │       │   │   ├── Plastic
│   │   │   │       │       │   │   │   ├── mat_end_BaseColor_plastic.png
│   │   │   │       │       │   │   │   ├── mat_end_Normal_plastic.png
│   │   │   │       │       │   │   │   ├── mat_end_OcclusionRoughnessMetallic_plastic.png
│   │   │   │       │       │   │   │   ├── mat_slide_BaseColor_plastic.png
│   │   │   │       │       │   │   │   ├── mat_slide_Normal_plastic.png
│   │   │   │       │       │   │   │   ├── mat_slide_OcclusionRoughnessMetallic_plastic.png
│   │   │   │       │       │   │   │   ├── mat_start_BaseColor_plastic.png
│   │   │   │       │       │   │   │   ├── mat_start_Normal_plastic.png
│   │   │   │       │       │   │   │   └── mat_start_OcclusionRoughnessMetallic_plastic.png
│   │   │   │       │       │   │   ├── Universal
│   │   │   │       │       │   │   │   ├── masks
│   │   │   │       │       │   │   │   │   ├── gradientMask.png
│   │   │   │       │       │   │   │   │   ├── water_ramp.png
│   │   │   │       │       │   │   │   │   └── water_ramp_2.png
│   │   │   │       │       │   │   │   ├── water
│   │   │   │       │       │   │   │   │   ├── Noise.PNG
│   │   │   │       │       │   │   │   │   ├── cloudsNoise .png
│   │   │   │       │       │   │   │   │   ├── endWater.png
│   │   │   │       │       │   │   │   │   ├── end_water_normal.png
│   │   │   │       │       │   │   │   │   ├── flowmap7.png
│   │   │   │       │       │   │   │   │   ├── flowmap8.png
│   │   │   │       │       │   │   │   │   ├── movingWater_AO.png
│   │   │   │       │       │   │   │   │   ├── movingWater_BC.png
│   │   │   │       │       │   │   │   │   ├── movingWater_H.png
│   │   │   │       │       │   │   │   │   ├── movingWater_N.png
│   │   │   │       │       │   │   │   │   ├── stagnantWater_AO.png
│   │   │   │       │       │   │   │   │   ├── stagnantWater_BC.png
│   │   │   │       │       │   │   │   │   ├── stagnantWater_H.png
│   │   │   │       │       │   │   │   │   ├── stagnantWater_N.png
│   │   │   │       │       │   │   │   │   ├── waterFallMask.png
│   │   │   │       │       │   │   │   │   └── waterFallMask2.png
│   │   │   │       │       │   │   │   ├── M_aquariumGlass_emissive.jpg
│   │   │   │       │       │   │   │   ├── mat_aquariumGlass_BaseColor.png
│   │   │   │       │       │   │   │   ├── mat_aquariumGlass_Emissive.png
│   │   │   │       │       │   │   │   ├── mat_aquariumGlass_Normal.png
│   │   │   │       │       │   │   │   ├── mat_aquariumGlass_OcclusionRoughnessMetallic.png
│   │   │   │       │       │   │   │   ├── mat_aquariumGlass_Opacity.png
│   │   │   │       │       │   │   │   ├── mat_lightsRim_BaseColor.png
│   │   │   │       │       │   │   │   ├── mat_lightsRim_Normal.png
│   │   │   │       │       │   │   │   ├── mat_lightsRim_OcclusionRoughnessMetallic.png
│   │   │   │       │       │   │   │   ├── mat_rainbowLights_BaseColor.png
│   │   │   │       │       │   │   │   ├── mat_rainbowLights_Normal.png
│   │   │   │       │       │   │   │   ├── mat_rainbowLights_OcclusionRoughnessMetallic.png
│   │   │   │       │       │   │   │   ├── mat_rainbowLights_emmissive.png
│   │   │   │       │       │   │   │   ├── mat_slideLights_BaseColor.png
│   │   │   │       │       │   │   │   ├── mat_slideLights_Normal.png
│   │   │   │       │       │   │   │   ├── mat_slideLights_OcclusionRoughnessMetallic.png
│   │   │   │       │       │   │   │   └── noise.png
│   │   │   │       │       │   │   └── Wood
│   │   │   │       │       │   │       ├── mat_end_BaseColor_wood.png
│   │   │   │       │       │   │       ├── mat_end_Normal_wood.png
│   │   │   │       │       │   │       ├── mat_end_OcclusionRoughnessMetallic_wood.png
│   │   │   │       │       │   │       ├── mat_slide_BaseColor_wood.png
│   │   │   │       │       │   │       ├── mat_slide_Normal_wood.png
│   │   │   │       │       │   │       ├── mat_slide_OcclusionRoughnessMetallic_wood.png
│   │   │   │       │       │   │       ├── mat_start_BaseColor_wood.png
│   │   │   │       │       │   │       ├── mat_start_Normal_wood.png
│   │   │   │       │       │   │       └── mat_start_OcclusionRoughnessMetallic_wood.png
│   │   │   │       │       │   ├── waterTest
│   │   │   │       │       │   │   ├── slide01_water.usd
│   │   │   │       │       │   │   └── slide02_water.usd
│   │   │   │       │       │   ├── EndParticles.usda
│   │   │   │       │       │   ├── EndPiece.usda
│   │   │   │       │       │   ├── FishMaterials.usda
│   │   │   │       │       │   ├── M_Glow.usda
│   │   │   │       │       │   ├── M_LightsRim.usda
│   │   │   │       │       │   ├── M_MovingWater.usda
│   │   │   │       │       │   ├── M_RainbowLights.usda
│   │   │   │       │       │   ├── M_SlideBottom.usda
│   │   │   │       │       │   ├── M_SlideLights.usda
│   │   │   │       │       │   ├── M_SlideTop.usda
│   │   │   │       │       │   ├── M_SolidSpheres.usda
│   │   │   │       │       │   ├── M_StagnantWater.usda
│   │   │   │       │       │   ├── M_WaterFall.usda
│   │   │   │       │       │   ├── M_endWater
│   │   │   │       │       │   ├── M_endWater.usda
│   │   │   │       │       │   ├── M_solidSpheres_emmissive.png
│   │   │   │       │       │   ├── Slide01.usda
│   │   │   │       │       │   ├── Slide02.usda
│   │   │   │       │       │   ├── Slide03.usda
│   │   │   │       │       │   ├── Slide04.usda
│   │   │   │       │       │   ├── Slide05.usda
│   │   │   │       │       │   ├── StartPiece.usda
│   │   │   │       │       │   ├── SwiftSplashTrackPieces.usda
│   │   │   │       │       │   ├── Untitled.usda
│   │   │   │       │       │   ├── WaterRideMaterials.usda
│   │   │   │       │       │   ├── distortion.usda
│   │   │   │       │       │   ├── glow_mask.png
│   │   │   │       │       │   ├── solidSpheres.usda
│   │   │   │       │       │   ├── solidSpheres.usdz
│   │   │   │       │       │   └── sphere_opacity.png
│   │   │   │       │       └── SwiftSplashTrackPieces.swift
│   │   │   │       ├── build
│   │   │   │       │   ├── EagerLinkingTBDs
│   │   │   │       │   │   └── Release-xros
│   │   │   │       │   ├── Release-xros
│   │   │   │       │   │   ├── PackageFrameworks
│   │   │   │       │   │   └── SwiftSplashTrackPieces_SwiftSplashTrackPieces.bundle
│   │   │   │       │   └── SwiftSplashTrackPieces.build
│   │   │   │       │       └── Release-xros
│   │   │   │       │           └── SwiftSplashTrackPieces_SwiftSplashTrackPieces.build
│   │   │   │       │               ├── DerivedSources
│   │   │   │       │               │   └── RealityAssetsGenerated
│   │   │   │       │               │       ├── CustomComponentUSDInitializers.usda
│   │   │   │       │               │       └── ModuleWithDependencies.json
│   │   │   │       │               ├── 7edbc1cc5cc2d7d899440c5ab7769731.sb
│   │   │   │       │               └── c9838f0f8c26148c3a159ab43e96009e.sb
│   │   │   │       ├── Package.swift
│   │   │   │       └── README.md
│   │   │   ├── SwiftSplash
│   │   │   │   ├── Assets
│   │   │   │   │   ├── deletePiece.wav
│   │   │   │   │   ├── endRide.wav
│   │   │   │   │   ├── fishSound_longLoudHappy.wav
│   │   │   │   │   ├── fishSound_mediumHappy.wav
│   │   │   │   │   ├── fishSound_quietHappy.wav
│   │   │   │   │   ├── pickUp.wav
│   │   │   │   │   ├── placePiece.wav
│   │   │   │   │   ├── startRide.wav
│   │   │   │   │   ├── swiftSplash_BuildMode.wav
│   │   │   │   │   ├── swiftSplash_Menu.wav
│   │   │   │   │   ├── swiftSplash_RideMode.m4a
│   │   │   │   │   └── waterFlowing.wav
│   │   │   │   ├── Assets.xcassets
│   │   │   │   │   ├── AccentColor.colorset
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── AppIcon.solidimagestack
│   │   │   │   │   │   ├── Back.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   └── SPIcon_bottom.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── Front.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   └── SPIcon_middle.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   ├── Middle.solidimagestacklayer
│   │   │   │   │   │   │   ├── Content.imageset
│   │   │   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   │   │   └── SPIcon_top.png
│   │   │   │   │   │   │   └── Contents.json
│   │   │   │   │   │   └── Contents.json
│   │   │   │   │   ├── goal_metal.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── goal_metal.png
│   │   │   │   │   ├── goal_plastic.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── goal_plastic.png
│   │   │   │   │   ├── goal_wood.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── goal_wood.png
│   │   │   │   │   ├── metalPreview.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── metalPreview@2x.png
│   │   │   │   │   ├── plasticPreview.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── plasticPreview@2x.png
│   │   │   │   │   ├── slide_01_metal.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_01_metal.png
│   │   │   │   │   ├── slide_01_plastic.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_01_plastic.png
│   │   │   │   │   ├── slide_01_wood.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_01_wood.png
│   │   │   │   │   ├── slide_02_metal.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_02_metal.png
│   │   │   │   │   ├── slide_02_plastic.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_02_plastic.png
│   │   │   │   │   ├── slide_02_wood.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_02_wood.png
│   │   │   │   │   ├── slide_03_metal.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_03_metal.png
│   │   │   │   │   ├── slide_03_plastic.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_03_plastic.png
│   │   │   │   │   ├── slide_03_wood.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_03_wood.png
│   │   │   │   │   ├── slide_04_metal.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_04_metal.png
│   │   │   │   │   ├── slide_04_plastic.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_04_plastic.png
│   │   │   │   │   ├── slide_04_wood.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_04_wood.png
│   │   │   │   │   ├── slide_05_metal.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_05_metal.png
│   │   │   │   │   ├── slide_05_plastic.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_05_plastic.png
│   │   │   │   │   ├── slide_05_wood.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── slide_05_wood.png
│   │   │   │   │   ├── swiftSplashHero.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── swiftSplashHero@2x.png
│   │   │   │   │   ├── woodPreview.imageset
│   │   │   │   │   │   ├── Contents.json
│   │   │   │   │   │   └── woodPreview@2x.png
│   │   │   │   │   └── Contents.json
│   │   │   │   ├── Data & State
│   │   │   │   │   ├── AppConfig.swift
│   │   │   │   │   ├── AppPhase.swift
│   │   │   │   │   ├── AppState+Phases.swift
│   │   │   │   │   ├── AppState+PieceLoading.swift
│   │   │   │   │   ├── AppState+PieceManagement.swift
│   │   │   │   │   ├── AppState+PieceSelection.swift
│   │   │   │   │   ├── AppState+RideRunning.swift
│   │   │   │   │   ├── AppState+TrackUpdates.swift
│   │   │   │   │   ├── AppState+Transparency.swift
│   │   │   │   │   ├── AppState.swift
│   │   │   │   │   ├── Piece.swift
│   │   │   │   │   └── SoundEffects.swift
│   │   │   │   ├── Extensions
│   │   │   │   │   ├── Date+Logging.swift
│   │   │   │   │   └── Entity+SwiftSplash.swift
│   │   │   │   ├── Preview Content
│   │   │   │   │   └── Preview Assets.xcassets
│   │   │   │   │       └── Contents.json
│   │   │   │   ├── Views
│   │   │   │   │   ├── Sources
│   │   │   │   │   │   └── Views
│   │   │   │   │   │       └── Views.rkassets
│   │   │   │   │   │           └── Scene.usda
│   │   │   │   │   ├── ContentToolbar.swift
│   │   │   │   │   ├── ContentView.swift
│   │   │   │   │   ├── EditTrackPieceView.swift
│   │   │   │   │   ├── ImageButton.swift
│   │   │   │   │   ├── PieceShelfTrackButtonsView.swift
│   │   │   │   │   ├── PieceShelfView.swift
│   │   │   │   │   ├── PlaceStartPieceView.swift
│   │   │   │   │   ├── RideControlView.swift
│   │   │   │   │   ├── SplashScreenView.swift
│   │   │   │   │   ├── TrackBuildingView+Drag.swift
│   │   │   │   │   ├── TrackBuildingView+Rotation.swift
│   │   │   │   │   ├── TrackBuildingView+Snapping.swift
│   │   │   │   │   └── TrackBuildingView.swift
│   │   │   │   ├── de.lproj
│   │   │   │   ├── fr.lproj
│   │   │   │   ├── ja.lproj
│   │   │   │   ├── ko.lproj
│   │   │   │   ├── zh_CN.lproj
│   │   │   │   ├── InfoPlist.xcstrings
│   │   │   │   ├── Localizable.xcstrings
│   │   │   │   └── SwiftSplashApp.swift
│   │   │   ├── SwiftSplash.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── SwiftSplash.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   ├── README.md
│   │   │   └── metadata.json
│   │   ├── tracking-specific-points-in-world-space
│   │   │   ├── Configuration
│   │   │   │   └── SampleCode.xcconfig
│   │   │   ├── ObjectPlacement
│   │   │   │   ├── 3D Models
│   │   │   │   │   ├── Box.usdz
│   │   │   │   │   ├── Cone.usdz
│   │   │   │   │   ├── Cube.usdz
│   │   │   │   │   └── Cylinder.usdz
│   │   │   │   ├── App
│   │   │   │   │   ├── AppState.swift
│   │   │   │   │   ├── DragState.swift
│   │   │   │   │   ├── PlaceableObject.swift
│   │   │   │   │   ├── PlacementManager.swift
│   │   │   │   │   └── PlacementState.swift
│   │   │   │   ├── Utilities
│   │   │   │   │   ├── GeometryUtilities.swift
│   │   │   │   │   ├── ModelLoader.swift
│   │   │   │   │   ├── PersistenceManager.swift
│   │   │   │   │   ├── PlaneAnchorHandler.swift
│   │   │   │   │   └── PlaneProjector.swift
│   │   │   │   ├── Views
│   │   │   │   │   ├── DeleteButton.swift
│   │   │   │   │   ├── HomeView.swift
│   │   │   │   │   ├── InfoLabel.swift
│   │   │   │   │   ├── ObjectPlacementMenuView.swift
│   │   │   │   │   ├── ObjectPlacementRealityView.swift
│   │   │   │   │   ├── ObjectSelectionView.swift
│   │   │   │   │   ├── PlacementTooltip.swift
│   │   │   │   │   └── TooltipView.swift
│   │   │   │   ├── Info.plist
│   │   │   │   └── ObjectPlacementApp.swift
│   │   │   ├── ObjectPlacement.xcodeproj
│   │   │   │   ├── project.xcworkspace
│   │   │   │   │   └── xcshareddata
│   │   │   │   │       ├── xcschemes
│   │   │   │   │       └── WorkspaceSettings.xcsettings
│   │   │   │   ├── xcshareddata
│   │   │   │   │   └── xcschemes
│   │   │   │   │       └── ObjectPlacement.xcscheme
│   │   │   │   └── project.pbxproj
│   │   │   ├── LICENSE.txt
│   │   │   └── README.md
│   │   └── visionos
│   │       └── project.zip
│   ├── urls
│   │   ├── discovered_urls.json
│   │   └── metadata.json
│   ├── analysis_results.json
│   └── doc_structure.json
├── docs
│   ├── api
│   │   ├── ANALYZERS.md
│   │   ├── CORE.md
│   │   ├── EXTRACTORS.md
│   │   └── MODELS.md
│   ├── guides
│   │   ├── CONTRIBUTING.md
│   │   ├── DEVELOPMENT.md
│   │   └── QUICKSTART.md
│   ├── technical
│   │   ├── ARCHITECTURE.md
│   │   ├── CACHING.md
│   │   ├── PATTERNS.md
│   │   └── RELATIONSHIPS.md
│   ├── CORE_FUNCTIONALITY.md
│   ├── INDEX.md
│   └── README.md
├── extractors
│   ├── __init__.py
│   ├── base_extractor.py
│   ├── code_extractor.py
│   ├── doc_extractor.py
│   ├── relationship_extractor.py
│   └── validation_extractor.py
├── models
│   ├── __init__.py
│   └── base.py
├── parsers
│   └── __init__.py
├── tests
│   ├── data
│   │   ├── accessing-the-main-camera.html
│   │   ├── adding-3d-content-to-your-app.html
│   │   ├── manifest_20241103_132703.json
│   │   ├── manifest_20241103_132746.json
│   │   ├── manifest_20241103_133041.json
│   │   ├── manifest_20241103_133244.json
│   │   ├── manifest_20241103_133425.json
│   │   ├── sample.html
│   │   ├── visionos_documentation_20241103_132703.json
│   │   ├── visionos_documentation_20241103_132746.json
│   │   ├── visionos_documentation_20241103_133041.json
│   │   ├── visionos_documentation_20241103_133244.json
│   │   └── visionos_documentation_20241103_133425.json
│   ├── output
│   ├── utils
│   │   └── examine_debug.py
│   ├── conftest.py
│   ├── examine_debug.py
│   ├── test_extractor_real.py
│   ├── test_extractors.py
│   ├── test_functionality.py
│   ├── test_pattern_refiner.py
│   ├── test_pattern_validation.py
│   ├── test_sample_view.py
│   └── test_url_access.py
├── tools
│   └── rollback.py
├── utils
│   ├── __init__.py
│   ├── cache_manager.py
│   └── logging.py
├── README.md
├── project_structure.md
├── pytest.ini
├── requirements.txt
├── run_scraper.py
└── setup.py

1593 directories, 3848 files
