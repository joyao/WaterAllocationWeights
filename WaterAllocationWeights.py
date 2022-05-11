#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import geopandas as gpd


def run():
    channel_list = ["./Data/InputData/公告幹線.shp", "./Data/InputData/支分線.shp"]
    merged_channel_shp, merged_channel_filepath = merge_channel_shp(channel_list, "merged_tunnel")
    nearest_shp, nearest_filepath = calc_nearest("./Data/InputData/稻作.shp", merged_channel_filepath)



def merge_channel_shp(data_list, output_filename="merged_tunnel"):
    merged_shp = []
    for d in data_list:
        channel_shp = gpd.read_file(d, encoding='utf8')
        if len(merged_shp) == 0:
            merged_shp = channel_shp
        else:
            merged_shp = merged_shp.append(channel_shp)
    output_filepath = "./Data/OutputData/%s.shp" % output_filename
    merged_shp.to_file(output_filepath, encoding='utf8')
    return merged_shp, output_filepath

def calc_nearest(left_shp_path, right_shp_path, output_filename="nearest_shp"):
    left_shp = gpd.read_file(left_shp_path, encoding='utf8')
    right_shp = gpd.read_file(right_shp_path, encoding='utf8')
    left_w_right_data = gpd.sjoin_nearest(left_shp, right_shp, distance_col="distance")
    output_filepath = "./Data/OutputData/%s.shp" % output_filename
    left_w_right_data.to_file(output_filepath, encoding='utf8')
    return left_w_right_data, output_filepath

if __name__ == '__main__':
    run()
