# スクリプト開始時刻
$startTime = Get-Date

# 実行するリクエストの数
$requestCount = 10

# 対象のURL
$flush_url = "http://138.2.40.146/flushall"
$url = "http://138.2.40.146/sorted-db-columns-cache"

# flush_urlに対してGETリクエストを実行してフラッシュする
Invoke-WebRequest -Uri $flush_url -Method Get -UseBasicParsing

# 同時実行するジョブの数
$concurrentTasks = 2

# ジョブを格納するための配列
$jobs = @()

for ($i = 0; $i -lt $requestCount; $i++) {
    # Invoke-WebRequestコマンドを非同期で実行し、ジョブを配列に追加
    $job = Start-Job -ScriptBlock {
        param($url)
        Invoke-WebRequest -Uri $url -Method Get -UseBasicParsing
    } -ArgumentList $url
    # Addメソッドを使用してジョブを追加
    $null = $jobs.Add($job)

    # 現在のジョブの数が$concurrentTasksに達したら、いずれかが終了するまで待機
    if ($jobs.Count -eq $concurrentTasks) {
        $finishedJob = Wait-Job -Job $jobs -Any
        # 終了したジョブを配列から削除
        $jobs = $jobs | Where-Object { $_.Id -ne $finishedJob.Id }
        # 終了したジョブを削除
        Remove-Job -Job $finishedJob
    }
}

# 残りのジョブが全て終了するまで待機
if ($jobs.Count -gt 0) {
    Wait-Job -Job $jobs
    Remove-Job -Job $jobs
}

# スクリプト終了時刻
$endTime = Get-Date

# 実行にかかった時間を計算
$duration = $endTime - $startTime

Write-Host "Test Complete"
Write-Host "Time: $($duration.TotalSeconds) sec"
