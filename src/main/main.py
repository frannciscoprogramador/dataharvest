from src.main.config.EdgeBrowser import EdgeBrowser
from src.main.config.Logger import Logger
from src.main.steps.Stories import Stories
from src.main.utils.Constants import BASE_URL, RESOURCES, PROFILES, DIV_STORES
from src.main.config.Postgres import Postgres

if __name__ == '__main__':
    logger = Logger('[            main           ]')
    sql = Postgres()
    # sql.create_profile_table()
    # sql.create_src_table()
    edge = EdgeBrowser()
    stories = Stories(edge, sql)
    for profile in PROFILES:
        exists_profile = sql.check_profile_exists(profile)
        if not exists_profile:
            sql.insert_profile(profile)
            logger.info(f'the insert was created for: {profile}')
        logger.info(f'the insert already exists for: {profile}')
        edge.open(f'{BASE_URL}{profile}')
        try:
            stories.access_store(RESOURCES, profile, DIV_STORES)
        except Exception as e:
            logger.info(f"An error occurred to stories: {e}")
        edge.open(f'{BASE_URL}{profile}')
        try:
            div_css_all_stories = stories.first_featured_stores()
            if div_css_all_stories:
                stories.access_store(RESOURCES, profile, div_css_all_stories)
        except Exception as e:
            logger.info(f"An error occurred to all stories: {e}")
    edge.close()
