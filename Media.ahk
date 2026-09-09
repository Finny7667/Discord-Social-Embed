#Requires AutoHotkey v2.0
#SingleInstance Force
#NoTrayIcon
Persistent()

; --- Configuration ---
LOG_FILE := "url_transformer_error.log"

; URL replacement patterns [Regex, Replacement]
global URL_PATTERNS := [
    ; 1. Pixiv daily ranking with date
    ["https://www\.pixiv\.net/ranking\.php\?date=\d+&mode=daily(?:_r18)?#ppixiv?(?:view=illust&)?illust_id=(\d+)&(?:view=illust&)?page=(\d+)", "https://www.phixiv.net/en/artworks/$1/$2"],
    
    ; 2. Pixiv daily ranking without date
    ["https://www\.pixiv\.net/ranking\.php\?mode=daily(?:_r18)?#ppixiv?(?:view=illust&)?illust_id=(\d+)&(?:view=illust&)?page=(\d+)", "https://www.phixiv.net/en/artworks/$1/$2"],
    
    ; 3. General Pixiv to Phixiv (UPDATED: Added ^# to exclude hash from capture, and (?:\#ppixiv)? to strip it)
    ["https://www\.pixiv\.net/([^#\s]+)(?:\#ppixiv)?", "https://www.phixiv.net/$1"],
    
    ; 4. Twitter/X to fixupxUPDATED: Added (\d+)(?:\?s=20) to exclude end
    ["https://x\.com/([^/]+)/status/(\d+)(?:\?s=20)?", "https://fixupx.com/$1/status/$2"],
    
    ; 5. Reddit to rxddit
    ["https://www\.reddit\.com/([^\s]+)", "https://www.vxreddit.com/$1"],
    
    ; 6. Bluesky to bskyx
    ["https://bsky\.app/([^\s]+)", "https://bskyx.app/$1"]
]

; --- Clipboard Monitoring ---
OnClipboardChange(ClipboardChanged)

ClipboardChanged(Type) {
    if (Type != 1)
        return

    try {
        originalText := A_Clipboard
        newText := originalText

        for pattern in URL_PATTERNS {
            newText := RegExReplace(newText, pattern[1], pattern[2])
        }

        if (newText != originalText) {
            A_Clipboard := newText
        }
    } catch as e {
        LogError(e.Message)
    }
}

; --- Logging Function ---
LogError(msg) {
    timestamp := FormatTime(, "yyyy-MM-dd HH:mm:ss")
    FileAppend(timestamp ": " msg "`n", LOG_FILE)
}

; --- EXIT HOTKEY ---
^!q::ExitApp() 
