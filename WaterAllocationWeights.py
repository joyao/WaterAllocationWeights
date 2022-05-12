#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import geopandas as gpd


def run():
    channel_list = ["./Data/InputData/公告幹線.shp", "./Data/InputData/支分線.shp"]
    merged_channel_shp, merged_channel_filepath = merge_channel_shp(
        channel_list, "merged_channel")
    nearest_shp, nearest_filepath = calc_nearest(
        "./Data/InputData/稻作.shp", merged_channel_filepath)


def merge_channel_shp(data_list, output_filename="merged_channel"):
    merged_shp = []
    for d in data_list:
        channel_shp = gpd.read_file(d, encoding='utf8')
        if len(merged_shp) == 0:
            merged_shp = channel_shp
        else:
            merged_shp = merged_shp.append(channel_shp)
    output_filepath = "./Data/OutputData/%s.shp" % output_filename
    geojson_filepath = "./Data/OutputData/%s.geojson" % output_filename
    merged_shp.to_file(output_filepath, encoding='utf8')
    merged_shp.to_file(geojson_filepath, encoding='utf8', driver="GeoJSON")
    return merged_shp, output_filepath


def calc_nearest(left_shp_path, right_shp_path, output_filename="nearest_shp"):
    left_shp = gpd.read_file(left_shp_path, encoding='utf8')
    right_shp = gpd.read_file(right_shp_path, encoding='utf8')
    left_w_right_data = gpd.sjoin_nearest(
        left_shp, right_shp, distance_col="distance")

    left_w_right_data = calc_weight(left_w_right_data, "distance", "distance")

    output_filepath = "./Data/OutputData/%s.shp" % output_filename
    geojson_filepath = "./Data/OutputData/%s.geojson" % output_filename
    left_w_right_data.to_file(output_filepath, encoding='utf8')
    left_w_right_data.to_file(
        geojson_filepath, encoding='utf8', driver="GeoJSON")
    return left_w_right_data, output_filepath


def calc_weight(gpd_data, column_name, calc_type):
    data = gpd_data[column_name]
    for k in data.keys():
        if (data[k].astype(int) == 0).all():
            data[k] = 0.0001
    weight = []
    if calc_type == "distance":
        weight = [1/float(d) for d in data]
    elif calc_type == "area":
        weight = [1/(float(d)**2) for d in data]
    gpd_data["weight"] = weight
    gpd_data["norm_w"] = normalized_weight(weight, 10000, 100)
    return gpd_data


def normalized_weight(data, infinity_value=10000, range=100):
    max_weight = max(filter(lambda d: d < infinity_value, data))
    min_weight = min(data)
    diff_weight = max_weight - min_weight
    count = 0
    for d in data:
        if d == infinity_value:
            data[count] = max_weight + diff_weight/range
        count += 1
    max_weight = max(data)
    rate = (range - 1)/(max_weight - min_weight)
    normalized_weight = [int(float(d)*rate + 1) for d in data]
    return normalized_weight


if __name__ == '__main__':
    run()
