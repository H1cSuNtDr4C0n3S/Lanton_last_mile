# alpha1 sweep status monitor
$ErrorActionPreference='SilentlyContinue'
Set-Location 'C:\Lanton_last_mile\alpha1'
$done=0
for($k=0;$k -lt 14;$k++){
  $l=Get-Content "log_shard$k.txt" -Tail 1
  if($l){ $done += [long]((($l -split ' ')[2]) -replace '/.*','') }
}
$hits=(Get-Content onsets_shard*.txt | Measure-Object).Count
$best=(Get-Content onsets_shard*.txt | ForEach-Object {[long]($_ -split ' ')[0]} | Measure-Object -Maximum).Maximum
$proc=(Get-Process alpha1_engine).Count
$start=[datetime](Get-Content run_started.txt)
$el=((Get-Date)-$start).TotalHours
$total=980000000
$eta=if($el -gt 0){ ($total-$done)/($done/$el)/1 } else {0}
Write-Output ("=== alpha1 sweep @ " + (Get-Date).ToString('HH:mm') + " ===")
Write-Output ("procs alive   : " + $proc + " / 14")
Write-Output ("elapsed       : " + [math]::Round($el,2) + " h")
Write-Output ("seeds done    : " + $done + " / " + $total + " (" + [math]::Round(100*$done/$total,1) + "%)")
Write-Output ("hits >=100k   : " + $hits)
Write-Output ("BEST onset    : " + $best + "  (sandbox max was 106258)")
Write-Output ("ETA remaining : ~" + [math]::Round($eta,1) + " h")
Write-Output ("top 5 onsets:")
Get-Content onsets_shard*.txt | Sort-Object {[long]($_ -split ' ')[0]} -Descending | Select-Object -First 5
