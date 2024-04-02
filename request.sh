#!/bin/bash

# スクリプト開始時刻
startTime=$(date +%s)

# 実行するリクエストの数
requestCount=100

# 対象のURL
url="http://138.2.40.146/sorted-db-columns-cache"

# 同時実行するプロセスの数
concurrentTasks=100

# タスクを格納するための配列
declare -a tasks

# 各リクエストに対して非同期でcurlコマンドを実行
for (( i=0; i<$requestCount; i++ )); do
  # curlコマンドをバックグラウンドで実行し、プロセスIDをtasks配列に追加
  curl -s -o /dev/null "$url" &
  tasks+=($!)

  # 現在のバックグラウンドプロセスの数が$concurrentTasksに達したら、
  # いずれかが終了するまで待機
  if [[ ${#tasks[@]} -eq $concurrentTasks ]]; then
    wait -n
    # 終了したプロセスを配列から削除
    tasks=("${tasks[@]/$!}")
  fi
done

# 残りのバックグラウンドプロセスが全て終了するまで待機
wait

# スクリプト終了時刻
endTime=$(date +%s)

# 実行にかかった時間を計算
duration=$((endTime - startTime))

echo "テスト完了"
echo "実行時間: $duration 秒"
