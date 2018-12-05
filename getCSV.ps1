Import-Module PSCrestron
try{
    Get-AutoDiscovery | export-csv "C:\Users\user\Desktop\devicesOnNetwork.csv"
} catch {
    $err = $_.Exception.Message
    echo $err
}
