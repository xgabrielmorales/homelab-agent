{
  description = "Development Environment";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };
  outputs = inputs: {
    devShells = builtins.mapAttrs (system: pkgs: {
      default = pkgs.mkShell {
        packages = [
          pkgs.uv
          pkgs.sops
          pkgs.age
        ];
      };
    }) inputs.nixpkgs.legacyPackages;
  };
}
