{ pkgs ? import
    (fetchTarball {
      name = "jpetrucciani-2025-04-25";
      url = "https://github.com/jpetrucciani/nix/archive/5a7cbdd8399da49b6b5aef239ed9a84687a6c9ab.tar.gz";
      sha256 = "02gnari6dnsrbz7frkjnx9bfqfzys185lnf8vrr07kgjby7dyzca";
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
