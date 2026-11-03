#!/usr/bin/env python3
"""Create the isolated, static UIKit demo project used by the rootless CI build."""

from pathlib import Path
import plistlib

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = REPOSITORY_ROOT / "SafeDemo"

FILES = {
    "Makefile": r"""TARGET = iphone:clang:latest:15.0
ARCHS = arm64
THEOS_PACKAGE_SCHEME = rootless

include $(THEOS)/makefiles/common.mk

APPLICATION_NAME = TrollDecryptAuditDemo
TrollDecryptAuditDemo_FILES = main.m AppDelegate.m ViewController.m
TrollDecryptAuditDemo_FRAMEWORKS = UIKit
TrollDecryptAuditDemo_RESOURCE_FILES = $(THEOS_PROJECT_DIR)/Info.plist
TrollDecryptAuditDemo_CFLAGS = -fobjc-arc
TrollDecryptAuditDemo_INSTALL_PATH = /Applications

include $(THEOS_MAKE_PATH)/application.mk
""",
    "control": r"""Package: com.jygg77.trolldecrypt-audit-demo
Name: TrollDecryptAuditDemo
Version: 0.1.0
Architecture: iphoneos-arm64
Description: Independent UIKit build-verification demo. Contains no decryption, hooks, process control, or app extraction.
Maintainer: jygg77
Author: jygg77
Section: Applications
Priority: optional
""",
    "Info.plist": r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>TrollDecryptAuditDemo</string>
    <key>CFBundleIdentifier</key>
    <string>com.jygg77.trolldecrypt-audit-demo</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>TrollDecryptAuditDemo</string>
    <key>CFBundleDisplayName</key>
    <string>Audit Demo</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>0.1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSRequiresIPhoneOS</key>
    <true/>
    <key>MinimumOSVersion</key>
    <string>15.0</string>
    <key>UIRequiredDeviceCapabilities</key>
    <array>
        <string>arm64</string>
    </array>
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
    </array>
</dict>
</plist>
""",
    "main.m": r"""#import <UIKit/UIKit.h>
#import "AppDelegate.h"

int main(int argc, char * argv[]) {
    @autoreleasepool {
        return UIApplicationMain(argc, argv, nil, NSStringFromClass([AppDelegate class]));
    }
}
""",
    "AppDelegate.h": r"""#import <UIKit/UIKit.h>

@interface AppDelegate : UIResponder <UIApplicationDelegate>
@property (strong, nonatomic) UIWindow *window;
@end
""",
    "AppDelegate.m": r"""#import "AppDelegate.h"
#import "ViewController.h"

@implementation AppDelegate

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    self.window = [[UIWindow alloc] initWithFrame:[UIScreen mainScreen].bounds];
    self.window.rootViewController = [ViewController new];
    [self.window makeKeyAndVisible];
    return YES;
}

@end
""",
    "ViewController.h": r"""#import <UIKit/UIKit.h>

@interface ViewController : UIViewController
@end
""",
    "ViewController.m": r"""#import "ViewController.h"

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    self.view.backgroundColor = UIColor.systemBackgroundColor;

    UILabel *title = [UILabel new];
    title.translatesAutoresizingMaskIntoConstraints = NO;
    title.text = @"Rootless build verification demo";
    title.font = [UIFont systemFontOfSize:24 weight:UIFontWeightBold];
    title.textColor = UIColor.labelColor;
    title.textAlignment = NSTextAlignmentCenter;
    title.numberOfLines = 0;

    UILabel *details = [UILabel new];
    details.translatesAutoresizingMaskIntoConstraints = NO;
    details.text = @"No decryption, hooks, process control or app extraction.";
    details.font = [UIFont systemFontOfSize:16 weight:UIFontWeightRegular];
    details.textColor = UIColor.secondaryLabelColor;
    details.textAlignment = NSTextAlignmentCenter;
    details.numberOfLines = 0;

    [self.view addSubview:title];
    [self.view addSubview:details];

    [NSLayoutConstraint activateConstraints:@[
        [title.leadingAnchor constraintEqualToAnchor:self.view.safeAreaLayoutGuide.leadingAnchor constant:24],
        [title.trailingAnchor constraintEqualToAnchor:self.view.safeAreaLayoutGuide.trailingAnchor constant:-24],
        [title.centerYAnchor constraintEqualToAnchor:self.view.centerYAnchor constant:-32],
        [details.topAnchor constraintEqualToAnchor:title.bottomAnchor constant:20],
        [details.leadingAnchor constraintEqualToAnchor:title.leadingAnchor],
        [details.trailingAnchor constraintEqualToAnchor:title.trailingAnchor]
    ]];
}

@end
""",
}

PROJECT_DIR.mkdir(parents=True, exist_ok=True)
for filename, contents in FILES.items():
    destination = PROJECT_DIR / filename
    destination.write_text(contents.lstrip(), encoding="utf-8")

with (PROJECT_DIR / "Info.plist").open("rb") as plist_file:
    metadata = plistlib.load(plist_file)

assert metadata["CFBundleIdentifier"] == "com.jygg77.trolldecrypt-audit-demo"
assert metadata["CFBundleExecutable"] == "TrollDecryptAuditDemo"
assert metadata["MinimumOSVersion"] == "15.0"

makefile = (PROJECT_DIR / "Makefile").read_text(encoding="utf-8")
assert "TARGET = iphone:clang:latest:15.0" in makefile
assert "THEOS_PACKAGE_SCHEME = rootless" in makefile
assert "ARCHS = arm64" in makefile

required_files = (
    "Makefile",
    "control",
    "Info.plist",
    "main.m",
    "AppDelegate.h",
    "AppDelegate.m",
    "ViewController.h",
    "ViewController.m",
)
for filename in required_files:
    if not (PROJECT_DIR / filename).is_file():
        raise SystemExit(f"Missing generated project file: {filename}")

print(f"Created and validated {len(required_files)} SafeDemo project files in {PROJECT_DIR}")
