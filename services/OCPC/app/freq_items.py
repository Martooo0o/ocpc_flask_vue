
# filter = dict with keys obj_type and value a list of attrs
def get_events_freq_fingerprints(events_df_row, filter, event_objs_df):
    fprint = []
    # print("Finding Fingerprint")
    # print(events_df_row)
    # print(event_objs_df.index)
    # print(filter)
    # print(filter[type])
    # print(events_df_row.kur)
    df = event_objs_df.copy()
    for obj_i in reversed(event_objs_df.index):
        if not event_objs_df.loc[obj_i]['object_id'] in events_df_row[event_objs_df.loc[obj_i]['object_type']]:
            df.drop(obj_i, inplace=True)

    # print("left objects to use")
    # print(df)

    for obj_i in df.index:
        if(event_objs_df.loc[obj_i]['object_type'] in filter.keys()):
            for attr in filter[event_objs_df.loc[obj_i]['object_type']]:
                # print('Obj keys')
                # print(event_objs_df.loc[obj_i].keys())
                if attr in event_objs_df.loc[obj_i].keys():
                    fprint.append(event_objs_df.loc[obj_i][attr])
    return fprint