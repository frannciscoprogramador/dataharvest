from src.main.config.EdgeBrowser import EdgeBrowser
from src.main.config.Logger import Logger
from src.main.steps.Stories import Stories
from src.main.steps.Posts import Posts
from src.main.utils.Constants import BASE_URL, RESOURCES, PROFILES, DIV_STORES
from src.main.config.Postgres import Postgres

if __name__ == '__main__':
    logger = Logger('[            main           ]')
    sql = Postgres()
    # sql.create_profile_table()
    # sql.create_src_table()
    edge = EdgeBrowser()
    stories = Stories(edge, sql)
    posts = Posts(edge, sql)
    for profile in PROFILES:
        exists_profile = sql.check_profile_exists(profile)
        # if not exists_profile:
        #     sql.insert_profile(profile)
        #
        # try:
        #     logger.info('step stories')
        #     edge.open(f'{BASE_URL}{profile}')
        #     stories.access_store(RESOURCES, profile, DIV_STORES)
        # except Exception as e:
        #     logger.info(f"error stories: {e}")
        #
        # try:
        #     logger.info('step all stories')
        #     edge.open(f'{BASE_URL}{profile}')
        #     div_css_all_stories = stories.first_featured_stores()
        #     if div_css_all_stories:
        #         stories.access_store(RESOURCES, profile, div_css_all_stories)
        # except Exception as e:
        #     logger.info(f"error all stories: {e}")

        try:
            logger.info('step posts')
            edge.open(f'{BASE_URL}{profile}')
            posts.posts(RESOURCES, profile)
        except Exception as e:
            logger.info(f"error stories: {e}")

    edge.close()
