test -e ssshtest || curl -fsSL https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest -o ssshtest
. ssshtest

PYTHON=${PYTHON:-python3}
tmp_dir=$(mktemp -d)
cleanup() {
	rm -f "$tmp_dir"/*.png
	rmdir "$tmp_dir"
}
trap cleanup EXIT

run test_plot_runs "$PYTHON" src/scatter.py --countries Brazil Canada China India --output-dir "$tmp_dir"
assert_exit_code 0

for country in brazil canada china india; do
	file_name="$tmp_dir/$country.png"
	assert_equal "$file_name" "$(ls "$file_name")"
done
