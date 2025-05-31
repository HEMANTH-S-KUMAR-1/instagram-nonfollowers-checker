import instaloader
import getpass

def find_non_followers(username: str, password: str):
    L = instaloader.Instaloader()

    try:
        print("Logging in...")
        L.login(username, password)
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        code = input("Enter 2FA code sent to your device: ")
        try:
            L.two_factor_login(code)
        except Exception as e:
            print(f"2FA login failed: {e}")
            return
    except instaloader.exceptions.BadCredentialsException:
        print("Error: Incorrect username or password.")
        return
    except Exception as e:
        print(f"Login failed: {e}")
        return

    try:
        print(f"Fetching profile data for @{username}...")
        profile = instaloader.Profile.from_username(L.context, username)

        print("Fetching followers...")
        followers = set(follower.username for follower in profile.get_followers())

        print("Fetching followees (accounts you follow)...")
        followees = set(followee.username for followee in profile.get_followees())

        not_following_back = followees - followers

        print(f"\nPeople who @{username} follows but who do NOT follow back:\n")

        if not not_following_back:
            print("🎉 Everyone you follow follows you back!")
        else:
            for user in sorted(not_following_back):
                print(user)

        # Save to a file
        with open("not_following_back.txt", "w", encoding="utf-8") as f:
            for user in sorted(not_following_back):
                f.write(user + "\n")

        print("\nList saved to 'not_following_back.txt'")

    except Exception as e:
        print(f"Failed to fetch data: {e}")

if __name__ == "__main__":
    username = input("Enter your Instagram username: ")
    password = getpass.getpass(f"Enter Instagram password for @{username}: ")
    find_non_followers(username, password)
