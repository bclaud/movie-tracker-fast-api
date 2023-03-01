{
  description = "A very basic python flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, }:
    flake-utils.lib.eachDefaultSystem (
      system: 
      let
        inherit (nixpkgs.lib) optional;
        pkgs = import nixpkgs {
          inherit system;
        };

        start = pkgs.writeScriptBin "start-app" "uvicorn main:app --reload";
      in
        with pkgs; rec {
          # packages = {};
          devShell = mkShell { name = "development-shell"; buildInputs = [ start pkgs.python311 poetry pkgs.python311Packages.poetry-core pkgs.python311Packages.black pkgs.python311Packages.pytest]; };
        }
    );
}


