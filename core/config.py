# Configuration settings
TESTING_MODE = True  # Set to False for full analysis
SKIP_DOWNLOADS = False  # Change this to False to enable downloads

# Test mode configuration
TEST_SAMPLE_COUNT = 3  # Number of samples to process in test mode
TEST_PATTERN_VALIDATION = True  # Validate patterns during test runs
PAGE_TIMEOUT = 60000  # Increase timeout to 60 seconds

# Cache settings
CACHE_DURATION = 24 * 60 * 60  # 24 hours in seconds
FORCE_DOWNLOAD = False  # Set to True to force re-download of samples

# Sample selection strategy
TEST_SAMPLE_STRATEGY = "diverse"  # Options: "first", "diverse", "random"

# Primary documentation URLs
BASE_URLS = [
    "https://developer.apple.com/documentation/visionos/",
    "https://developer.apple.com/design/human-interface-guidelines/immersive-experiences",
    "https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos"
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