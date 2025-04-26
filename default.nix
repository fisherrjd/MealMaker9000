{ pkgs ? import
    (fetchTarball {
      name = "jpetrucciani-2025-03-07";
      url = "https://github.com/jpetrucciani/nix/archive/b14e48596c71f40e02f909698e458b91a00e7827.tar.gz";
      sha256 = "0cq995j8p9xdqrxxk4k2civby44pmkc1khzhmnzcndmwkwyvjk8m";
    })
    { }
}:
let
  name = "MealMaker9000";

  uvEnv = pkgs.uv-nix.mkEnv {
    inherit name; python = pkgs.python313;
    workspaceRoot = ./.;
    pyprojectOverrides = final: prev: { };
  };

  tools = with pkgs; {
    cli = [
      jfmt
      nixup
    ];

    uv = [ uv uvEnv ];
    rust = [
      cargo
      clang
      rust-analyzer
      rustc
      rustfmt
      # deps
      pkg-config
      openssl
    ];
    scripts = pkgs.lib.attrsets.attrValues scripts;
  };

  scripts = with pkgs; { };
  paths = pkgs.lib.flatten [ (builtins.attrValues tools) ];
  env = pkgs.buildEnv {
    inherit name paths; buildInputs = paths;
  };
in
(env.overrideAttrs (_: {
  inherit name;
  NIXUP = "0.0.9";
} // uvEnv.uvEnvVars)) // { inherit scripts; }
