import logging
#from autochannel import db
from flask import current_app as app
from autochannel.models import Guild, Category

LOG = logging.getLogger(__name__)

def data_update_guild_categories(guild_id, categories):
    """data_update_guild_categories checks the difference between categories
    from the discord api and the Database. Then will run delete any categories 
    that have been removed and add any that have been created
    
    Arguments:
        guild_id {string} -- Guild ID
        categories {dictionary} -- Dictionary of categories from the discord API
        from the guild 
    """
    cats = list(Category.query.with_entities(Category.id).filter_by(guild_id=guild_id).all())
    cats = [i[0] for i in cats]
    """This converts a list of tuples to a list for my own sanity
    """
    existing_cats = [int(c) for c in categories]
    """Creates a list of existing cats in discord
    """
    miss_cats = set(existing_cats).difference(cats)
    delete_cats = set(cats).difference(existing_cats)

    update_categories =  True if len(miss_cats ) > 0 or len(delete_cats) > 0 else False
    """Only want to run a db commit if there is any changes """

    for mc in miss_cats:
        cat_id_add = Category(id=mc, guild_id=guild_id)
        app.db.add(cat_id_add)
        LOG.debug(f'Adding category: {categories[str(mc)]["name"]} to guild: {guild_id}')        

    for dc in delete_cats: 
        cat_id_delete = Category.query.get(dc)
        app.db.delete(cat_id_delete)
        LOG.debug(f'Deleting category: {dc} that no longer exists in the Guild')

    if update_categories:
        db.session.commit()

# def add_category(id, guild_id, name=)