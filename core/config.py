from pathlib import Path

# Configuration settings
TESTING_MODE = False  # Set to False for full analysis
SKIP_DOWNLOADS = False  # Enable downloads

# Test mode configuration
TEST_SAMPLE_COUNT = 3  # Number of samples to process in test mode
TEST_PATTERN_VALIDATION = True  # Validate patterns during test runs
SKIP_URL_DISCOVERY = False  # Set to False to enable URL discovery
PAGE_TIMEOUT = 60000  # Increase timeout to 60 seconds

# Cache settings
CACHE_DURATION = 24 * 60 * 60  # 24 hours in seconds
FORCE_DOWNLOAD = True  # Force re-download of documentation

# Documentation crawling settings
MAX_CRAWL_DEPTH = 3  # Maximum depth for documentation page crawling
DOCUMENTATION_CACHE_DIR = Path("data/documentation_cache")
DOCUMENTATION_CONTENT_DIR = DOCUMENTATION_CACHE_DIR / "content"
DOCUMENTATION_CONTENT_CACHE = DOCUMENTATION_CACHE_DIR / "content_cache.json"
DEBUG_DIR = Path("data/debug")

# Sample selection strategy
TEST_SAMPLE_STRATEGY = "arkit_first"  # Options: "first", "diverse", "random", "arkit_first"

# Add ARKit-specific samples to prioritize
ARKIT_SAMPLES = [
    'ExploringObjectTrackingWithARKit',
    'BuildingLocalExperiencesWithRoomTracking',
    'ObjectPlacementExample',
    'SceneReconstructionExample'
]

# Primary documentation URLs
BASE_URLS = [
    "https://developer.apple.com/documentation/visionos/",
    "https://developer.apple.com/design/human-interface-guidelines/immersive-experiences",
    "https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos",
    "https://developer.apple.com/visionos/",
    "https://developer.apple.com/documentation/realitykit/",
    "https://developer.apple.com/documentation/arkit/",
    "https://developer.apple.com/documentation/swiftui/",
    "https://developer.apple.com/documentation/spatial/"
]

# Known sample projects
KNOWN_SAMPLES = [
    '/world',
    '/hello-world',
    '/bot-anist',
    '/playing-spatial-audio',
    '/diorama',
    '/destination-video',
    '/food-truck',
    '/happy-beam',
    '/solar-system'
]

# Pattern types
PATTERN_TYPES = [
    'ui_components',
    'immersive_spaces',
    'spatial_audio',
    'animation',
    'gestures',
    '3d_content',
    'arkit'
]

# Framework-specific documentation sections
REALITYKIT_SECTIONS = {
    'Scene Understanding': {
        'url': 'https://developer.apple.com/documentation/realitykit/realitykit-scene-understanding',  # Note: Constructed URL - needs verification
        'required_children': [
            'sceneunderstandingcomponent',
            'entitytype',
            'origin',
            'options'
        ],
        'relationships': {
            'parent': None,
            'children': {
                'sceneunderstandingcomponent': {
                    'type': 'class',
                    'relationships': ['entitytype', 'origin', 'options']
                },
                'entitytype': {
                    'type': 'enum',
                    'relationships': ['sceneunderstandingcomponent']
                },
                'origin': {
                    'type': 'enum',
                    'relationships': ['sceneunderstandingcomponent']
                },
                'options': {
                    'type': 'struct',
                    'relationships': ['sceneunderstandingcomponent']
                }
            }
        }
    },
    'Entity Actions': {
        'url': 'https://developer.apple.com/documentation/realitykit/ecs-entity-actions',  # Note: Constructed URL - needs verification
        'required_children': [
            'entityaction',
            'actionanimation',
            'actionevent',
            'actioneventtype',
            'actionentityresolution'
        ],
        'relationships': {
            'parent': None,
            'children': {
                'entityaction': {
                    'type': 'protocol',
                    'relationships': ['actionanimation', 'actionevent', 'actioneventtype']
                },
                'actionanimation': {
                    'type': 'class',
                    'relationships': ['entityaction', 'actionevent']
                },
                'actionevent': {
                    'type': 'struct',
                    'relationships': ['entityaction', 'actionanimation', 'actioneventtype']
                },
                'actioneventtype': {
                    'type': 'enum',
                    'relationships': ['actionevent']
                },
                'actionentityresolution': {
                    'type': 'struct',
                    'relationships': ['entityaction']
                }
            }
        }
    },
    'Entity Components': {
        'url': 'https://developer.apple.com/documentation/realitykit/component-implementations',  # Note: Constructed URL - needs verification
        'required_children': [
            'modelcomponent',
            'collisioncomponent',
            'physicsmotioncomponent',
            'anchoringcomponent',
            'synchronizationcomponent'
        ],
        'relationships': {
            'parent': None,
            'children': {
                'modelcomponent': {
                    'type': 'class',
                    'relationships': []
                },
                'collisioncomponent': {
                    'type': 'class',
                    'relationships': ['physicsmotioncomponent']
                },
                'physicsmotioncomponent': {
                    'type': 'class',
                    'relationships': ['collisioncomponent']
                },
                'anchoringcomponent': {
                    'type': 'class',
                    'relationships': []
                },
                'synchronizationcomponent': {
                    'type': 'class',
                    'relationships': []
                }
            }
        }
    }
}

# Documentation validation settings
VALIDATION_SETTINGS = {
    'min_code_examples': 2,
    'required_sections': [
        'Overview',
        'Parameters',
        'Return Value',
        'See Also'
    ],
    'verify_relationships': True,
    'check_broken_links': True,
    'relationship_rules': {
        'framework': ['class', 'protocol', 'struct', 'enum'],
        'class': ['method', 'property', 'enum'],
        'protocol': ['method', 'property'],
        'struct': ['method', 'property', 'enum'],
        'enum': ['case', 'method', 'property']
    }
}