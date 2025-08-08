import instaloader
import getpass
import json
import time
from datetime import datetime
from typing import Set, Optional

class InstagramAnalyzer:
    def __init__(self):
        self.loader = instaloader.Instaloader()
        
    def login(self, username: str, password: str) -> bool:
        """Login to Instagram with enhanced error handling."""
        try:
            print("🔐 Logging in...")
            self.loader.login(username, password)
            print("✅ Login successful!")
            return True
            
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            return self._handle_2fa()
            
        except instaloader.exceptions.BadCredentialsException:
            print("❌ Error: Incorrect username or password.")
            return False
            
        except instaloader.exceptions.ConnectionException:
            print("❌ Error: Connection failed. Please check your internet connection.")
            return False
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    def _handle_2fa(self) -> bool:
        """Handle two-factor authentication."""
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                code = input("📱 Enter 2FA code sent to your device: ").strip()
                self.loader.two_factor_login(code)
                print("✅ 2FA authentication successful!")
                return True
            except Exception as e:
                remaining = max_attempts - attempt - 1
                if remaining > 0:
                    print(f"❌ 2FA failed: {e}. {remaining} attempts remaining.")
                else:
                    print(f"❌ 2FA failed after {max_attempts} attempts: {e}")
        return False
    
    def get_followers_and_followees(self, username: str) -> tuple[Set[str], Set[str], dict]:
        """Fetch followers and followees with progress tracking."""
        try:
            print(f"👤 Fetching profile data for @{username}...")
            profile = instaloader.Profile.from_username(self.loader.context, username)
            
            # Profile stats
            stats = {
                'followers_count': profile.followers,
                'following_count': profile.followees,
                'posts_count': profile.mediacount,
                'full_name': profile.full_name,
                'is_private': profile.is_private
            }
            
            if profile.is_private and profile.followed_by_viewer is False:
                print("⚠️  This account is private and you don't follow it.")
                return set(), set(), stats
            
            print(f"📊 Profile Stats: {stats['followers_count']} followers, {stats['following_count']} following")
            
            # Fetch followers
            print("📥 Fetching followers... (this may take a while)")
            followers = set()
            try:
                for i, follower in enumerate(profile.get_followers()):
                    followers.add(follower.username)
                    if (i + 1) % 100 == 0:
                        print(f"   Fetched {i + 1} followers...")
                        time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"⚠️  Warning: Could not fetch all followers: {e}")
            
            # Fetch followees
            print("📤 Fetching people you follow... (this may take a while)")
            followees = set()
            try:
                for i, followee in enumerate(profile.get_followees()):
                    followees.add(followee.username)
                    if (i + 1) % 100 == 0:
                        print(f"   Fetched {i + 1} accounts you follow...")
                        time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"⚠️  Warning: Could not fetch all followees: {e}")
            
            return followers, followees, stats
            
        except instaloader.exceptions.ProfileNotExistsException:
            print(f"❌ Error: Profile @{username} does not exist.")
            return set(), set(), {}
        except Exception as e:
            print(f"❌ Failed to fetch data: {e}")
            return set(), set(), {}
    
    def analyze_followers(self, username: str, password: str, save_results: bool = True):
        """Main function to analyze followers."""
        # Login
        if not self.login(username, password):
            return
        
        # Get data
        followers, followees, stats = self.get_followers_and_followees(username)
        
        if not followers and not followees:
            print("❌ No data could be retrieved.")
            return
        
        # Analysis
        not_following_back = followees - followers
        following_back = followees & followers
        not_followed_by_you = followers - followees
        
        # Results
        print("\n" + "="*60)
        print(f"📈 ANALYSIS RESULTS FOR @{username}")
        print("="*60)
        print(f"👥 Total followers: {len(followers)}")
        print(f"➡️  Total following: {len(followees)}")
        print(f"💔 Not following you back: {len(not_following_back)}")
        print(f"💚 Following you back: {len(following_back)}")
        print(f"🆕 Following you but you don't follow: {len(not_followed_by_you)}")
        
        if not_following_back:
            print(f"\n📋 People who don't follow you back ({len(not_following_back)}):")
            print("-" * 40)
            for user in sorted(not_following_back):
                print(f"  @{user}")
        else:
            print("\n🎉 Everyone you follow follows you back!")
        
        # Save results
        if save_results and (not_following_back or not_followed_by_you):
            self.save_results(username, not_following_back, not_followed_by_you, 
                            following_back, stats)
    
    def save_results(self, username: str, not_following_back: Set[str], 
                    not_followed_by_you: Set[str], following_back: Set[str], 
                    stats: dict):
        """Save analysis results to files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed JSON report
        report = {
            'username': username,
            'timestamp': timestamp,
            'stats': stats,
            'analysis': {
                'not_following_back': sorted(list(not_following_back)),
                'not_followed_by_you': sorted(list(not_followed_by_you)),
                'mutual_follows': sorted(list(following_back)),
                'summary': {
                    'not_following_back_count': len(not_following_back),
                    'not_followed_by_you_count': len(not_followed_by_you),
                    'mutual_follows_count': len(following_back)
                }
            }
        }
        
        json_filename = f"instagram_analysis_{username}_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Save simple text file for not following back
        if not_following_back:
            txt_filename = f"not_following_back_{username}_{timestamp}.txt"
            with open(txt_filename, 'w', encoding='utf-8') as f:
                f.write(f"People who @{username} follows but who do NOT follow back:\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                for user in sorted(not_following_back):
                    f.write(f"@{user}\n")
            print(f"\n💾 Results saved to:")
            print(f"   📄 {txt_filename}")
        
        print(f"   📊 {json_filename}")

def main():
    """Main function with improved user interaction."""
    print("=" * 60)
    print("📱 INSTAGRAM FOLLOWER ANALYZER")
    print("=" * 60)
    print("This tool helps you find who doesn't follow you back on Instagram.")
    print("⚠️  Note: This may take several minutes for accounts with many followers/following.")
    print()
    
    analyzer = InstagramAnalyzer()
    
    try:
        username = input("Enter your Instagram username: ").strip()
        if not username:
            print("❌ Username cannot be empty.")
            return
        
        password = getpass.getpass(f"Enter Instagram password for @{username}: ")
        if not password:
            print("❌ Password cannot be empty.")
            return
        
        save_choice = input("Save results to files? (y/n, default: y): ").strip().lower()
        save_results = save_choice != 'n'
        
        print("\n🚀 Starting analysis...")
        analyzer.analyze_followers(username, password, save_results)
        
    except KeyboardInterrupt:
        print("\n\n❌ Analysis cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()