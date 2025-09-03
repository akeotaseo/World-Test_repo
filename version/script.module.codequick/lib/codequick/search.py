from __future__ import absolute_import
from hashlib import sha1
from codequick import localized
from codequick.storage import PersistentDict
from codequick.support import dispatcher
from codequick.listing import Listitem
from codequick.utils import keyboard, ensure_unicode
from codequick.route import Route, validate_listitems
import pickle
SEARCH_DB = u"_new_searches.pickle"
class Search(object):
    def __init__(self, plugin, extra_params):
        self.db = search_db = PersistentDict(SEARCH_DB)
        plugin.register_delayed(search_db.close)
        session_hash = self.hash_params(extra_params)
        self.data = search_db.setdefault(session_hash, [])
    def __iter__(self):
        return iter(self.data)
    def __contains__(self, item):
        return item in self.data
    def __bool__(self):
        return bool(self.data)
    def __nonzero__(self):
        return bool(self.data)
    def remove(self, item):
        self.data.remove(item)
        self.db.flush()
    def append(self, item):
        self.data.append(item)
        self.db.flush()
    @staticmethod
    def hash_params(data):
        sorted_dict = sorted(data.items())
        content = pickle.dumps(sorted_dict, protocol=2)
        return ensure_unicode(sha1(content).hexdigest())
@Route.register
def saved_searches(plugin, remove_entry=None, search=False, first_load=False, **extras):
    searchdb = Search(plugin, extras)
    if remove_entry and remove_entry in searchdb:
        searchdb.remove(remove_entry)
        plugin.update_listing = True
    elif search or (first_load and not searchdb):
        search_term = keyboard(plugin.localize(localized.ENTER_SEARCH_STRING))
        if search_term:
            return redirect_search(plugin, searchdb, search_term, extras)
        elif not searchdb:
            return False
        else:
            plugin.update_listing = True
    return list_terms(plugin, searchdb, extras)
def redirect_search(plugin, searchdb, search_term, extras):
    plugin.params[u"_title_"] = title = search_term.title()
    plugin.category = title
    callback_params = extras.copy()
    callback_params["search_query"] = search_term
    route = callback_params.pop("_route")
    dispatcher.selector = route
    func = dispatcher.get_route().function
    listitems = func(plugin, **callback_params)
    valid_listitems = validate_listitems(listitems)
    if valid_listitems:
        if search_term not in searchdb:
            searchdb.append(search_term)
        return valid_listitems
    else:
        return False
def list_terms(plugin, searchdb, extras):
    search_item = Listitem()
    search_item.label = f"[B]{plugin.localize(localized.SEARCH)}[/B]"
    search_item.set_callback(saved_searches, search=True, **extras)
    search_item.art.global_thumb("search_new.png")
    yield search_item
    callback_params = extras.copy()
    route = callback_params.pop("_route")
    callback = dispatcher.get_route(route).callback
    str_remove = plugin.localize(localized.REMOVE)
    for search_term in searchdb:
        item = Listitem()
        item.label = search_term.title()
        item.context.container(saved_searches, str_remove, remove_entry=search_term, **extras)
        item.params.update(callback_params, search_query=search_term)
        item.set_callback(callback)
        yield item