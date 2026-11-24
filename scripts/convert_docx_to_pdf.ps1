param (
    [string]$docxPath = "A:\DEV\projectz\coal\BIT_Mesra_Project_Report.docx",
    [string]$pdfPath = "A:\DEV\projectz\coal\BIT_Mesra_Project_Report.pdf"
)

Write-Host "Converting $docxPath to $pdfPath using Microsoft Word..."

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = [Microsoft.Office.Interop.Word.WdAlertLevel]::wdAlertsNone

try {
    $doc = $word.Documents.Open($docxPath, $false, $true)
    # wdExportFormatPDF = 17
    $doc.ExportAsFixedFormat($pdfPath, 17)
    $doc.Close([Microsoft.Office.Interop.Word.WdSaveOptions]::wdDoNotSaveChanges)
    Write-Host "Successfully exported PDF: $pdfPath"
}
catch {
    Write-Error "Error during conversion: $_"
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
