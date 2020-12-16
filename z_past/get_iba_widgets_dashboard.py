# --- import ---
import shared
import json

l = shared.blueprint()
token = l[0]
bp_id = l[1]
bp_iba_widgets_get = shared.bp_iba_widgets_get(token, bp_id)
bp_iba_dashboards_get = shared.bp_iba_dashboards_get(token, bp_id)

# Get IBA Widgets from BP
def get_iba_widgets():
    for i in bp_iba_widgets_get['items']:
        del i['created_at'],i['updated_at'],i['id'],i['updated_by']
        with open('iba_widgetes.json','w') as f:
            f.write(json.dumps(bp_iba_widgets_get))

def get_iba_dashboard():
    for i in bp_iba_dashboards_get['items']:
        del i['created_at'],i['updated_at'],i['id'],i['updated_by'],i['predefined_dashboard']
        with open('iba_dashboard.json','w') as f:
            f.write(json.dumps(bp_iba_dashboards_get))

get_iba_widgets()
get_iba_dashboard()
