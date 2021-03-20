
let
  mach-nix = import (builtins.fetchGit {
    url = "https://github.com/DavHau/mach-nix/";
    ref = "refs/tags/3.1.1";  # update this version
  }) {
    python = "python38";
  };
in { pkgs ? import <nixpkgs> {} }:
mach-nix.mkPythonShell {  
    requirements = builtins.readFile ./requirements.txt;
}
