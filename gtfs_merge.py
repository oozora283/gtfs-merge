'''
【複数GTFS-JPデータセットの統合】
・agency/agency_jp 接頭辞の付加に伴う一部属性置換
・routes 接頭辞付加
・stops 接頭辞付加 （他事業者近傍停留所のグループ化は実行しない）
・calendar 接頭辞付加 
・fare_rules 接頭辞付加

引数1 データセットが格納されているディレクトリ
'''

import sys
import os
import glob
import csv
import shutil

args = sys.argv

path = args[1]
dir_list = []
entry_list = []

def set_prefix(entnum, entmax):
    alphabet = [chr(i) for i in range(65, 65+26)]
    if entmax <= 26:
        return (alphabet[entnum])
    else:
        return (alphabet[int(entnum/26)]+alphabet[entnum%26])

def main():
    dir_list = sorted(glob.glob(path+'*/'))

    merge_startday = merge_endday = None
    for dirs in dir_list:
        startday_tag = endday_tag = None
        if os.path.isfile(dirs+'feed_info.txt'):
            with open(dirs + 'feed_info.txt', encoding='utf_8_sig') as feed_fp:
                reader = csv.reader(feed_fp)
                feed_dt = [row for row in reader]
            for headtag in range(len(feed_dt[0])):
                if feed_dt[0][headtag] == 'feed_start_date':
                    startday_tag = headtag
                elif feed_dt[0][headtag] == 'feed_end_date':
                    endday_tag = headtag

            startday = int(feed_dt[1][startday_tag])
            endday = int(feed_dt[1][endday_tag])
            
            print(dirs.lstrip(path), startday, endday)
            judge = None
            while True:
                judge = input('Add？ [Y/N] ')
                if judge == 'Y' or judge == 'y':
                    entry_list.append(dirs)
                    if startday_tag!=-1:
                        if merge_startday == None or startday>merge_startday:
                            merge_startday = startday
                    if endday_tag!=-1:
                        if merge_endday == None or endday<merge_endday:
                            merge_endday = endday
                    break
                elif judge == 'N' or judge == 'n':
                    break
            print()


    table_list = ['agency', 'agency_jp', 'routes', 'routes_jp', 'office_jp', 'shapes', 'calendar','calendar_dates', 'trips', 'frequencies', 'stops', 'fare_attributes', 'fare_rules', 'transfers', 'stop_times', 'translations']
    out = [[['agency_id', 'agency_number', 'agency_name', 'agency_url', 'agency_timezone', 'agency_lang', 'agency_phone', 'agency_fare_url', 'agency_email']],
            [['agency_id','agency_official_name', 'agency_zip_number', 'agency_address', 'agency_president_pos', 'agency_president_name']],
            [['route_id', 'agency_id', 'route_short_name', 'route_long_name', 'route_desc', 'route_type', 'route_url', 'route_color', 'route_text_color', 'jp_parent_route_id']],
            [['route_id', 'route_update_date', 'origin_stop', 'via_stop', 'destination_stop']],
            [['office_id', 'office_name', 'office_url', 'office_phone']],
            [['shape_id', 'shape_pt_lat', 'shape_pt_lon', 'shape_pt_sequence', 'shape_dist_traveled']],
            [['service_id', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'start_date', 'end_date']],
            [['service_id', 'date', 'exception_type']],
            [['route_id', 'service_id', 'trip_id', 'trip_headsign', 'trip_short_name', 'direction_id', 'block_id', 'shape_id', 'wheelchair_accessible', 'bikes_allowed', 'jp_trip_desc', 'jp_trip_desc_symbol', 'jp_office_id']],
            [['trip_id', 'start_time', 'end_time', 'headway_secs', 'exact_times']],
            [['stop_id', 'stop_code', 'stop_name', 'stop_desc', 'stop_lat', 'stop_lon', 'zone_id', 'stop_url', 'location_type', 'parent_station', 'stop_timezone', 'wheelchair_boarding', 'platform_code']],
            [['fare_id', 'price', 'currency_type', 'payment_method', 'transfers', 'transfer_duration']],
            [['fare_id', 'route_id', 'origin_id', 'destination_id', 'contains_id']],
            [['from_stop_id', 'to_stop_id', 'transfer_type', 'min_transfer_time']],
            [['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence', 'stop_headsign', 'pickup_type', 'drop_off_type', 'shape_dist_traveled', 'timepoint']],
            [['trans_id', 'lang', 'translation']]]
    id_list = [[None],[None],[0],[0],[0],[0],[0],[0],[0,1,2,6,7,12],[0],[0,6,9],[0],[0,1,2,3],[0,1],[0,3],[None]]
    memo = []
    trans_id_dict = {}


    if os.path.isdir('merge'):
        shutil.rmtree('merge')
    os.mkdir('merge')

    for entnum,entname in enumerate(entry_list):
        prefix = set_prefix(entnum, len(entry_list))
        for tblnum,tblname in enumerate(table_list):
            tblpath = entname+tblname+'.txt'
            dtag = [-1] * len(out[tblnum][0])
            dt = []
            if os.path.isfile(tblpath):
                with open(tblpath, encoding='utf_8_sig') as fp:
                    reader = csv.reader(fp)
                    dt = [row for row in reader]
                for tagnum, tagname in enumerate(out[tblnum][0]):
                    for dtagnum,dtagname in enumerate(dt[0]):
                        if dtagname == tagname:
                            dtag[tagnum] = dtagnum

                if tblname == 'agency':
                    # 'agency_id'を接頭辞で置き換える
                    # 置き換え前の'agency_id'は'agency_number'とする
                    dt[1].append(dt[1][dtag[0]])
                    dt[1][dtag[0]] = prefix
                    dtag[1] = max(dtag) + 1
                    memo.append([prefix,entname,dt[1][dtag[2]]])
                if tblname == 'agency_jp':
                    dt[1][dtag[0]] = prefix
                if tblname == 'routes':
                    for row in range(len(dt)):
                        dt[row][dtag[1]] = prefix
                for row in range(1, len(dt)):
                    if tblname == 'translations':
                        if dt[row][dtag[0]] not in trans_id_dict.keys():
                            trans_id_dict[dt[row][dtag[0]]] = [True,True,True]
                        if dt[row][dtag[1]] == 'ja':
                            if trans_id_dict[dt[row][dtag[0]]][0]:
                                trans_id_dict[dt[row][dtag[0]]][0] = False
                                out[tblnum].append([dt[row][dtag[i]] if dtag[i] != -1 else '' for i in range(len(out[tblnum][0]))])
                        elif dt[row][dtag[1]] == 'en':
                            if trans_id_dict[dt[row][dtag[0]]][1]:
                                trans_id_dict[dt[row][dtag[0]]][1] = False
                                out[tblnum].append([dt[row][dtag[i]] if dtag[i] != -1 else '' for i in range(len(out[tblnum][0]))])
                        elif dt[row][dtag[1]] == 'ja-Hrkt':
                            if trans_id_dict[dt[row][dtag[0]]][2]:
                                trans_id_dict[dt[row][dtag[0]]][2] = False
                                out[tblnum].append([dt[row][dtag[i]] if dtag[i] != -1 else '' for i in range(len(out[tblnum][0]))])
                    else:
                        for col in range(len(out[tblnum][0])):
                            if col in id_list[tblnum]:
                                if dtag[col] != -1 and dt[row][dtag[col]] != '':
                                    dt[row][dtag[col]] = prefix + dt[row][dtag[col]]
                        out[tblnum].append([dt[row][dtag[i]] if dtag[i] != -1 else '' for i in range(len(out[tblnum][0]))])


    for tblnum, tblname in enumerate(table_list):
        with open('merge/' + tblname + '.txt', 'w',encoding='utf_8_sig') as fp:
            writer = csv.writer(fp, lineterminator='\n')
            writer.writerows(out[tblnum]) 

    with open('merge/feed_info.txt', 'w',encoding='utf_8_sig') as fp:
        writer = csv.writer(fp, lineterminator='\n')
        writer.writerows([['feed_publisher_name', 'feed_publisher_url', 'feed_lang', 'feed_start_date', 'feed_end_date', 'feed_version'],['GTFS-JP統合ツール(T.Takase)','','ja',merge_startday,merge_endday,'']]) 

    with open('memo.txt', 'w',encoding='utf_8_sig') as io:
        writer = csv.writer(io, lineterminator='\n')
        writer.writerows(memo)


if __name__ == '__main__':
    main()
    sys.exit(0)
