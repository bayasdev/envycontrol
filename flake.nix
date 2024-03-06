{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      packages.${system} = {
        envycontrol = pkgs.python3Packages.buildPythonPackage {
          pname = "envycontrol";
          version = "3.4.0";
          src = self;
        };
        default = self.packages.${system}.envycontrol;
      };

      buildInputs = with pkgs; [ pciutils ];

      devShells.default = pkgs.mkShellNoCC {
        packages = with pkgs; [
          (python3.withPackages(ps: with ps; [ setuptools ]))
          pciutils
        ];
      };
    };
}
