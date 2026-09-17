param(
    [ValidateSet('doctor','build','client','server','data','blockbench','nbt','idea')]
    [string]$Action = 'doctor'
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$configFile = Join-Path $PSScriptRoot 'local.json'
if (!(Test-Path -LiteralPath $configFile)) { throw 'Copy tooling/local.example.json to tooling/local.json and configure local paths.' }
$config = Get-Content -LiteralPath $configFile -Raw | ConvertFrom-Json
function Resolve-ToolPath([string]$value) {
    if ([IO.Path]::IsPathRooted($value)) { return $value }
    return [IO.Path]::GetFullPath((Join-Path $projectRoot $value))
}
$jdk = Resolve-ToolPath $config.javaHome
if (!(Test-Path -LiteralPath (Join-Path $jdk 'bin/java.exe'))) { throw "JDK not found: $jdk" }
if ($Action -eq 'doctor') {
    & (Join-Path $jdk 'bin/java.exe') -version
    $toolRows = foreach ($entry in $config.executables.PSObject.Properties) {
        $resolved = Resolve-ToolPath $entry.Value
        [pscustomobject]@{ Tool=$entry.Name; Available=(Test-Path -LiteralPath $resolved); Path=$resolved }
    }
    $toolRows | Format-Table -AutoSize | Out-Host
    exit 0
}
if ($Action -in @('blockbench','nbt','idea')) {
    $exe = Resolve-ToolPath $config.executables.$Action
    if (!(Test-Path -LiteralPath $exe)) { throw "Tool not found: $exe" }
    $launch = @{ FilePath=$exe; WorkingDirectory=$projectRoot }
    if ($Action -eq 'idea') { $launch.ArgumentList = '"' + $projectRoot + '"' }
    if ($Action -eq 'nbt') { $launch.ArgumentList = '"' + (Join-Path $projectRoot 'art/nbt/development-sample.nbt') + '"' }
    # These are the interactive tools explicitly selected by the user.
    $previousRollForward = $env:DOTNET_ROLL_FORWARD
    try {
        if ($Action -eq 'nbt' -and $config.nbtRollForward) { $env:DOTNET_ROLL_FORWARD=$config.nbtRollForward }
        Start-Process @launch
    } finally { $env:DOTNET_ROLL_FORWARD=$previousRollForward }
    exit 0
}
$oldJava = $env:JAVA_HOME
$oldPath = $env:PATH
Push-Location $projectRoot
try {
    $env:JAVA_HOME = $jdk
    $env:PATH = "$jdk\bin;$env:PATH"
    $tasks = @{build='build'; client='runClient'; server='runServer'; data='runData'}
    & (Join-Path $projectRoot 'gradlew.bat') $tasks[$Action] '--console=plain'
    $result = $LASTEXITCODE
} finally {
    $env:JAVA_HOME = $oldJava
    $env:PATH = $oldPath
    Pop-Location
}
exit $result
