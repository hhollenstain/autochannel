import logging
from autochannel import db
from autochannel.models import Guild, Category

LOG = logging.getLogger(__name__)

def data_update_guild_categories(guild_id, categories):
    """[summary]
    
    Arguments:
        guild_id {[type]} -- [description]
        categories {[type]} -- [description]
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


    if len(miss_cats) > 0 or len(delete_cats) > 0:
        update_categories = True
    else:
        update_categories = False

    LOG.info(miss_cats)
    for mc in miss_cats:
        cat_id_add = Category(id=mc, guild_id=guild_id, name=categories[str(mc)]['name'])
        db.session.add(cat_id_add)
        LOG.debug(f'Adding category: {categories[str(mc)]["name"]} to guild: {guild_id}')        

    for dc in delete_cats: 
        cat_id_delete = Category.query.get(dc)
        db.session.delete(cat_id_delete)
        LOG.debug(f'Deleting category: {dc} that no longer exists in the Guild')

    if update_categories:
        db.session.commit()