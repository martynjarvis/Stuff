import XMonad
import XMonad.Config.Gnome
import XMonad.Hooks.ManageDocks
import XMonad.Hooks.ManageHelpers
import XMonad.Layout.NoBorders
import XMonad.Layout.Gaps
import XMonad.Hooks.EwmhDesktops
import XMonad.Hooks.FadeInactive
import XMonad.Actions.CycleWS 

myWorkspaces = ["1:work1","2:work2","3:work3","4:work4","5:root","6:spotify","7:skype","8:doc","9:web" ]

myManageHook = composeAll
     [ className =? "Firefox"     --> doShift "9:web"
     , className =? "Evince"      --> doShift "8:doc"
     , className =? "Spotify"     --> doShift "6:spotify"
     , className =? "Skype"       --> doShift "7:skype"
     , className =? "Canvas"      --> doFloat
     , className =? "Canvas"      --> doShift "5:root"
     , className =? "Browser"     --> doFloat
     , className =? "Browser"     --> doShift "5:root"
     , className =? "net-sourceforge-jnlp-runtime-Boot"     --> doFloat --evo
     , isFullscreen               --> doFullFloat
     , className =? "Unity-2d-launcher" --> doIgnore
     , className =? "Unity-2d-panel"    --> doIgnore
     , className =? "Do"          --> doFloat
     ]

myLayouts = gaps [(U, 24)] $ layoutHook gnomeConfig

main =  xmonad $ gnomeConfig
    { 
    terminal = "gnome-terminal"
    , workspaces = myWorkspaces
    , manageHook = myManageHook <+> manageHook gnomeConfig
    , layoutHook = myLayouts
    -- ,layoutHook = smartBorders (layoutHook gnomeConfig)
    --, layoutHook = smartBorders (avoidStruts $ layoutHook gnomeConfig)
    , focusFollowsMouse = False
    }
