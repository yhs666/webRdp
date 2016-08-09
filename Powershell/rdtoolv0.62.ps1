#yanghongsheng Created 2015/12/7

$file_path = "\\tsclient\E\robbot\"
#$file_path = "E:\robbot\"

Add-Type -AssemblyName System.Windows.Forms

cd  $HOME\RDTools
./RDEnv.cmd
cd  .\rd_cmt_stable*
#Cd   Fabric
$Env:path=$Env:Path+";.;$pwd.Path"

#cd $HOME

notepad
osk.exe

# clear clipboard
function Clear-Clipboard {
   Add-Type -AssemblyName System.Windows.Forms
   [System.Windows.Forms.Clipboard]::Clear()
   Write-Output "Clipboard cleared."
}


Clear-Clipboard
Write-Output "Please copy command,It's Will run in powershell!! "

function  toclipboard{
    $mmss = Get-Date -Format m:s
    #$tocli = ("done:" + $mmss).Trim(" .-`t`n`r")
    $tocli = "done:" + $mmss
    Pscx\Set-Clipboard -Text   $tocli

    #Write-Clipboard  $tocli -NoNewLine

}

function getclipboard {
    #$z =(Get-Clipboard -Format Text)
    $z = Pscx\Get-Clipboard -Text 
    return $z

}

#create thread pool
$throttleLimit = 40
$SessionState = [system.management.automation.runspaces.initialsessionstate]::CreateDefault()
$Pool = [runspacefactory]::CreateRunspacePool(1, $throttleLimit, $SessionState, $Host)
$Pool.Open()

$p =$pwd
Write-Host $p
#define scriptblock

$ScriptBlock = {

    param($dict,$handlers,$file_path,$p)

    #dict{name，path,cmd}
    # name --> file name
    #path -->command path
    #cmd --> run command
    #handler -->  thread handlers

    try {
            # run command
            $name =$file_path + $dict.name
            $hash = $dict.name
			cd $p
            cd $dict.path
            $cmd0 = $dict.cmd
           
            write-host "run cmd: $cmd0, file: $name"
            #Invoke-Expression -Command  "$cmd0   2>&1 > $hash" -OutVariable 
            Invoke-Expression -Command  "$cmd0" -OutVariable $hash
            (Get-Variable $hash).Value | Out-File -Encoding default $hash

            xcopy /y $hash  $file_path
            write-host "$cmd0 done"
    }
    Catch [Exception] {
  
        # catch the thread error
        $ErrorMessage = $_.Exception.Message
        $FailedItem = $_.Exception.ItemName
        Write-Host "eeeoe"
        Write-Host $ErrorMessage,$FailedItem
        Set-content -path $name  -value "$ErrorMessage,$FailedItem!." 
        #Add-Content -path $name  -value "$ErrorMessage,$FailedItem!." 
    }
    finally {
             # run done, close the thread
             $i = 0
              foreach ($handle in $handles) {
                    if ($handle -ne $null) {
                          if ($handle.IsCompleted) {
                                #$threads[$i].EndInvoke($handle)
                                $threads[$i].Dispose()
                                write-host "Close processing ID $i"
                                $handles[$i] = $null
                          }
                    }

                    $i++
              }
    }
}


$threads = @()

#set run location
Set-Location $pwd
[System.IO.Directory]::SetCurrentDirectory("$pwd")

$starttime = Get-date

toclipboard

while($true){

     toclipboard
    Start-Sleep -s 1
   
    Write-Output   "Waiting command!" 

    #got from clipboard
    $get_cmds = getclipboard
    write-host $get_cmds

    if ("done" -in $get_cmds){
        continue
    }else{

        try{
	        $get_cmds = getclipboard |  ConvertFrom-Json

        }
        catch [Exception]{
            $get_cmds=$null
            continue

        }
    }
 
    # run command
    if($get_cmds  ){

        $check_cmd = $get_cmds[0].psobject.properties.name

        if(($check_cmd.Count -eq 3) -and ("name" -in $check_cmd ) -and ("path" -in $check_cmd ) -and ("cmd" -in $check_cmd )){
                $handles = foreach ($cmd_dict in $get_cmds) {

				    $powershell = [powershell]::Create().AddScript($ScriptBlock).AddArgument($cmd_dict).AddArgument($handles).AddArgument($file_path).AddArgument($p)
				    $powershell.RunspacePool = $Pool
				    $powershell.BeginInvoke()
		
				    $threads += $powershell
				    }
                    #set-Clipboard -Value "done"
                    toclipboard
          }else{
            		Write-output "Command check issue!!"
                    

          }

	}
}


