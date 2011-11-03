import XMonad
import XMonad.Config.Gnome
import XMonad.Hooks.ManageDocks
import XMonad.Hooks.ManageHelpers
import XMonad.Layout.NoBorders
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
     , className =? "Canvas"      --> doShift "5:root"      --TCanvas
     , className =? "Browser"     --> doFloat
     , className =? "Browser"     --> doShift "5:root"      --TBrowser 
     , className =? "net-sourceforge-jnlp-runtime-Boot" --> doFloat --evo
     , isFullscreen               --> doFullFloat
     ]

--Fading
--myLogHook :: X()
--myLogHook = fadeInactiveLogHook fadeAmount
--    where fadeAmount = 0.8

main =  xmonad $ gnomeConfig
    { 
    terminal = "gnome-terminal --hide-menubar"
    , workspaces = myWorkspaces
    , manageHook = myManageHook <+> manageDocks <+> manageHook gnomeConfig
    -- ,manageHook = myManageHook <+> manageHook gnomeConfig
    , layoutHook = smartBorders (avoidStruts $ layoutHook gnomeConfig)
    -- ,layoutHook = smartBorders (layoutHook gnomeConfig)
--    , logHook = myLogHook
--   ,handleEventHook = fullscreenEventHook <+> handleEventHook gnomeConfig
--above line fixes fullscreen videos for multi-screen setups, but only in
--v>0.9.1 or contrib setup
    }
