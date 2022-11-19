$ScriptDir = split-path -parent $MyInvocation.MyCommand.Definition

& ./clang-format.exe --dump-config                  > (Join-Path $ScriptDir "_clang-format_default")
& ./clang-format.exe --dump-config --style chromium > (Join-Path $ScriptDir "_clang-format_chromium")
& ./clang-format.exe --dump-config --style google   > (Join-Path $ScriptDir "_clang-format_google")
& ./clang-format.exe --dump-config --style llvm     > (Join-Path $ScriptDir "_clang-format_llvm")
& ./clang-format.exe --dump-config --style mozilla  > (Join-Path $ScriptDir "_clang-format_mozilla")
& ./clang-format.exe --dump-config --style webkit   > (Join-Path $ScriptDir "_clang-format_webkit")

& ./clang-tidy.exe  --dump-config > (Join-Path $ScriptDir "_clang-tidy")