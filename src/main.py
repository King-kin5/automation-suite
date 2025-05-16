from platforms.instagram.bot import InstagramBot


def main():
    """Main entry point for the social media automation tool"""
    try:
        # Initialize and run the Instagram bot
        bot = InstagramBot()
        bot.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
