{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "python-dev-shell";

  packages = with pkgs; [
    python312
    python312Packages.pip
    pyright
  ];

  shellHook = ''
    echo "🐍 Python dev shell ready!"
  '';
}