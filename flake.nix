{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      pkgs = forAllSystems (system: nixpkgs.legacyPackages.${system});
    in
    {
      packages = forAllSystems (system:
        with pkgs.${system}.python3Packages; {
          default = buildPythonPackage rec {
            name = "envycontrol";
            version = "3.3.1";
            src = self;
          };
      });

      devShells = forAllSystems (system: let
      in {
        default = pkgs.${system}.mkShellNoCC {
          packages = with pkgs.${system}; [
            python3
          ];
        };
      });
    };
}
