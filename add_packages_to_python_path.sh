PWD=$(pwd)
PACKAGES=("miles_apps")

for pkg in "${PACKAGES[@]}"; do
    pkg_path="$PWD/$pkg"
    case ":$PYTHONPATH:" in
        *":$pkg_path:"*) ;;  # already present → skip
        *) export PYTHONPATH="$pkg_path:$PYTHONPATH" ;;
    esac
done

echo "DONE"
