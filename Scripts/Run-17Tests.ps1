# RimWorld 1.7 unstable, test-only Ironmaking core/production Pickle runner.
# Never rebuild production or change public About.xml/Defs; 1.6 Python runner stays intact.
[CmdletBinding()]
param(
    [string]$GameRoot = 'D:\SteamLibrary\steamapps\common\RimWorld',
    [ValidateSet('Vanilla','MO','All')][string]$Profile = 'Vanilla',
    [ValidateSet('core','production')][string]$Suite = 'core',
    [ValidateRange(60,3600)][int]$TimeoutSeconds = 300
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'RimWorldRuntime.ps1')
$game = Get-RimWorldRuntime $GameRoot
if (-not $game.Modern) { throw 'Use run-pickle-e2e.bat for RimWorld 1.6.' }
$repo = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$mods = Join-Path $game.Root 'Mods'
$normal = Join-Path $env:USERPROFILE 'AppData/LocalLow/Ludeon Studios/RimWorld by Ludeon Studios/Config'
$hashes = @{}
foreach ($name in @('ModsConfig.xml','Prefs.xml')) {
    $hashes[$name] = (Get-FileHash -LiteralPath (Join-Path $normal $name) -Algorithm SHA256).Hash
}
[xml]$about = Get-Content -LiteralPath (Join-Path $repo 'About/About.xml') -Raw
$identity = 'sucro.ancientmedievaljapan.ironmaking'
if ([string]$about.ModMetaData.packageId -ne $identity) { throw 'Unexpected Ironmaking source packageId.' }
$source = $repo
$sourceFixture = Join-Path $mods 'AMJI.TestSource17'
$testFixture = Join-Path $mods 'AMJI.TestPickle17'
foreach ($folder in @($sourceFixture,$testFixture)) {
    if (Test-Path -LiteralPath $folder) { throw "Stale test fixture requires inspection: $folder" }
}
$actualSourceInMods = ([IO.Path]::GetFullPath((Split-Path -Parent $repo)) -eq [IO.Path]::GetFullPath($mods))
if (-not $actualSourceInMods) {
    foreach ($dir in (Get-ChildItem -LiteralPath $mods -Directory)) {
        $candidate = Join-Path $dir.FullName 'About/About.xml'
        if (Test-Path -LiteralPath $candidate) {
            try { [xml]$entry = Get-Content -LiteralPath $candidate -Raw }
            catch { continue }
            if ([string]$entry.ModMetaData.packageId -eq $identity) {
                throw 'Another Ironmaking source is installed. Run from that exact source to avoid duplicate packageIds.'
            }
        }
    }
}
$workshop = [IO.Path]::GetFullPath((Join-Path $game.Root '../../workshop/content/294100'))
$quick = Find-RimWorldModAssembly (Join-Path $workshop '3793646067') 'Quickstarts.dll' '1.7'
$pickle = Find-RimWorldModAssembly (Join-Path $workshop '3791648678') 'RimWorks.Pickle.dll' '1.7'
$result = Join-Path $repo ('TestResults/Ironmaking17-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
New-Item -ItemType Directory -Force -Path $result | Out-Null
$owned = New-Object 'System.Collections.Generic.List[string]'
try {
    if (-not $actualSourceInMods) {
        New-Item -ItemType Directory -Path $sourceFixture | Out-Null
        $owned.Add($sourceFixture)
        Set-Content -LiteralPath (Join-Path $sourceFixture '.AMJI-17-OWNED') -Value 'Ironmaking source' -Encoding Ascii
        foreach ($folder in @('About','Defs','Patches','Assemblies','Textures','Languages')) {
            $from = Join-Path $repo $folder
            if (Test-Path -LiteralPath $from) { Copy-Item -LiteralPath $from -Destination $sourceFixture -Recurse }
        }
        [xml]$sourceAbout = Get-Content -LiteralPath (Join-Path $sourceFixture 'About/About.xml') -Raw
        $versions = $sourceAbout.SelectSingleNode('/ModMetaData/supportedVersions')
        if ($null -eq $versions) { throw 'Missing source supportedVersions node.' }
        $li = $sourceAbout.CreateElement('li')
        $li.InnerText = '1.7'
        [void]$versions.AppendChild($li)
        $sourceAbout.Save((Join-Path $sourceFixture 'About/About.xml'))
        $source = $sourceFixture
    }
    New-Item -ItemType Directory -Path $testFixture | Out-Null
    $owned.Add($testFixture)
    Set-Content -LiteralPath (Join-Path $testFixture '.AMJI-17-OWNED') -Value 'Ironmaking tests' -Encoding Ascii
    foreach ($folder in @('About','Assemblies','Pickle/Assemblies','Pickle/Features','Strings')) {
        New-Item -ItemType Directory -Force -Path (Join-Path $testFixture $folder) | Out-Null
    }
    [xml]$testAbout = Get-Content -LiteralPath (Join-Path $repo 'Tests/E2E/TestMod/About/About.xml') -Raw
    $testAbout.ModMetaData.packageId = 'sucro.ancientmedievaljapan.ironmaking.e2e17'
    $versions = $testAbout.SelectSingleNode('/ModMetaData/supportedVersions')
    $li = $testAbout.CreateElement('li'); $li.InnerText = '1.7'; [void]$versions.AppendChild($li)
    $testAbout.Save((Join-Path $testFixture 'About/About.xml'))
    Copy-Item -Path (Join-Path $repo 'Tests/E2E/TestMod/Pickle/Features/*.feature') -Destination (Join-Path $testFixture 'Pickle/Features')
    Set-Content -LiteralPath (Join-Path $testFixture 'Strings/AMJI-17.txt') -Value 'Temporary Pickle test marker' -Encoding Ascii

    function Get-TestSources([string]$project) {
        [xml]$doc = Get-Content -LiteralPath $project -Raw
        $base = Split-Path -Parent $project
        @($doc.SelectNodes('//Compile') | ForEach-Object {
            $file = Join-Path $base ([string]$_.Include)
            if (-not (Test-Path -LiteralPath $file)) { throw "Missing Ironmaking test source: $file" }
            $file
        })
    }
    Invoke-RimWorldTestCompile $game.Root (Join-Path $testFixture 'Assemblies/AMJ.Ironmaking.Quickstarts.dll') `
        (Get-TestSources (Join-Path $repo 'Tests/E2E/Quickstarts.csproj')) @($quick)
    Invoke-RimWorldTestCompile $game.Root (Join-Path $testFixture 'Pickle/Assemblies/AMJ.Ironmaking.PickleSteps.dll') `
        (Get-TestSources (Join-Path $repo 'Tests/E2E/Steps.csproj')) @($pickle)

    $profiles = if ($Profile -eq 'All') { @('Vanilla','MO') } else { @($Profile) }
    foreach ($name in $profiles) {
        $folder = Join-Path $result $name
        $report = Join-Path $folder 'Reports'
        $configDir = Join-Path $folder 'SaveData/Config'
        New-Item -ItemType Directory -Force -Path $configDir | Out-Null
        [xml]$config = Get-Content -LiteralPath (Join-Path $normal 'ModsConfig.xml') -Raw
        $active = $config.SelectSingleNode('/ModsConfigData/activeMods')
        if ($null -eq $active -or $null -eq $config.SelectSingleNode('/ModsConfigData/knownExpansions')) {
            throw 'Normal source config lacks activeMods/knownExpansions; refusing synthetic DLC context.'
        }
        $active.RemoveAll()
        $ids = @('brrainz.harmony','ludeon.rimworld','rimworks.rimlogging','rimworks.pickle','rimworks.quickstarts')
        if ($name -eq 'MO') {
            $ids += @('oskarpotocki.vanillafactionsexpanded.core','syrchalis.processor.framework',
                'dankpyon.medieval.overhaul')
        }
        $ids += @($identity,'sucro.ancientmedievaljapan.ironmaking.e2e17')
        foreach ($id in $ids) {
            $li = $config.CreateElement('li'); $li.InnerText = $id
            [void]$active.AppendChild($li)
        }
        $config.ModsConfigData.version = $game.Version.Split(' ')[0]
        $config.Save((Join-Path $configDir 'ModsConfig.xml'))
        [xml]$prefs = Get-Content -LiteralPath (Join-Path $normal 'Prefs.xml') -Raw
        foreach ($pair in @(@('devMode','True'),@('resetModsConfigOnCrash','False'),@('fullscreen','False'),@('runInBackground','True'))) {
            $node = $prefs.DocumentElement.SelectSingleNode($pair[0])
            if ($null -eq $node) { $node = $prefs.CreateElement($pair[0]); [void]$prefs.DocumentElement.AppendChild($node) }
            $node.InnerText = $pair[1]
        }
        $prefs.Save((Join-Path $configDir 'Prefs.xml'))
        New-Item -ItemType Directory -Force -Path $report | Out-Null
        $env:AMJI_EXPECTED_PROFILE = $name
        $env:AMJI_EXPECTED_SOURCE_ROOT = $source
        $env:AMJI_PROGRESS_PATH = Join-Path $report 'step-progress.txt'
        $arguments = '-savedatafolder="' + (Split-Path -Parent $configDir) + '" -pickle-run="ironmaking-' +
            $Suite + '.feature" -pickle-mode=fast -pickle-set-name="' + $name +
            '" -pickle-report-dir="' + $report +
            '" -pickle-no-browser -pickle-no-http -pickle-run-timeout=4 -pickle-retry=0'
        Invoke-RimWorldIsolated $game.Root $arguments (Join-Path $report 'Player.log') $TimeoutSeconds
        $python = (Get-Command python -ErrorAction Stop).Source
        & $python (Join-Path $repo 'Scripts/validate_pickle_result.py') --report $report --suite $Suite
        if ($LASTEXITCODE -ne 0) { throw "Ironmaking 1.7 Pickle validator failed: $name" }
        Write-Output "[OK] Ironmaking $($game.Version) $name/$Suite; native ERROR 0: $report"
    }
}
finally {
    foreach ($name in @('AMJI_EXPECTED_PROFILE','AMJI_EXPECTED_SOURCE_ROOT','AMJI_PROGRESS_PATH')) {
        Remove-Item "Env:$name" -ErrorAction SilentlyContinue
    }
    foreach ($folder in @($owned | Select-Object -Unique)) {
        $marker = Join-Path $folder '.AMJI-17-OWNED'
        if (-not (Test-Path -LiteralPath $marker) -or
            (Get-Content -LiteralPath $marker -Raw).Trim() -notin @('Ironmaking source','Ironmaking tests')) {
            throw "Refusing unsafe Ironmaking cleanup: $folder"
        }
        Remove-Item -LiteralPath $folder -Recurse -Force
    }
    foreach ($name in $hashes.Keys) {
        if ((Get-FileHash -LiteralPath (Join-Path $normal $name) -Algorithm SHA256).Hash -ne $hashes[$name]) {
            throw "Normal $name changed during Ironmaking 1.7 test."
        }
    }
}
