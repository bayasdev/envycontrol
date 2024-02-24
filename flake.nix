{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.poetry2nix.url = "github:nix-community/poetry2nix";

  outputs = { self, nixpkgs, poetry2nix }:
    let
      supportedSystems = [ "x86_64-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      pkgs = forAllSystems (system: nixpkgs.legacyPackages.${system});
    in
    {
      packages = forAllSystems (system: let
        inherit (poetry2nix.lib.mkPoetry2Nix { pkgs = pkgs.${system}; }) mkPoetryScriptsPackage;
      in {
        default = mkPoetryScriptsPackage { 
          projectDir = self;
        };
      });

      devShells = forAllSystems (system: let
        inherit (poetry2nix.lib.mkPoetry2Nix { pkgs = pkgs.${system}; }) mkPoetryEnv;
      in {
        default = pkgs.${system}.mkShellNoCC {
          packages = with pkgs.${system}; [
            (mkPoetryEnv { 
              projectDir = self;
            })
            poetry
          ];
        };
      });
    };
}
