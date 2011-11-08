import XMonad
import XMonad.Config.Gnome
--- Hooks
import XMonad.Hooks.ManageDocks
import XMonad.Hooks.ManageHelpers
import XMonad.Hooks.EwmhDesktops
import XMonad.Hooks.DynamicLog
import XMonad.Hooks.FadeInactive
--- Layouts
import XMonad.Layout
import XMonad.Layout.Grid
import XMonad.Layout.Circle
import XMonad.Layout.IM
import XMonad.Layout.NoBorders
import XMonad.Layout.PerWorkspace
import XMonad.Layout.ResizableTile
import XMonad.Layout.StackTile
import XMonad.Layout.Tabbed
import XMonad.Layout.Gaps
--- System
--import System
--import System.Environment
--import System.IO
--- Utils
--import XMonad.Util.EZConfig
import Data.Ratio ((%))


--import XMonad.Actions.CycleWS 

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



-- Layouts
--myLayouts = gaps [(U, 24)] $ layoutHook gnomeConfig
myLayout = gaps [(U,24)] $ avoidStruts $ onWorkspace "7:skype" imLayout $ standardLayouts 
  where
    -- define the list of standardLayouts
    standardLayouts = tiled ||| Mirror tiled ||| Circle |||  Full ||| simpleTabbed

    -- notice withIM is acting on it
    imLayout = withIM (1%7) skypeRoster Grid

    -- default tiling algorithm partitions the screen into two panes
    tiled = Tall nmaster delta ratio

    -- The default number of windows in the master pane
    nmaster = 1

    -- Default proportion of screen occupied by master pane
    ratio = 4/7

    -- Percent of screen to increment by when resizing panes
    delta = 3/100

    skypeRoster = (ClassName "Skype") `And` (Not (Title "Options")) `And` (Not (Role "Chats")) `And` (Not (Role "CallWindowForm"))
 
--Fading
myLogHook :: X()
myLogHook = fadeInactiveLogHook fadeAmount
    where fadeAmount = 0.8

main =  xmonad $ gnomeConfig
    { 
    terminal = "gnome-terminal"
    , workspaces = myWorkspaces
    , manageHook = myManageHook <+> manageHook gnomeConfig
    , layoutHook = smartBorders(myLayout)
    -- ,layoutHook = smartBorders (layoutHook gnomeConfig)
    --, layoutHook = smartBorders (avoidStruts $ layoutHook gnomeConfig)
    --, logHook = logHook gnomeConfig >> fadeInactiveLogHook 0xcccccccc
    , logHook = myLogHook
    , focusFollowsMouse = False
    }
