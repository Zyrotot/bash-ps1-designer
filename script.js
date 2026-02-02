const ANSI_STYLES = {
    // Regular
    "Black":  {"code": "0;30", "fg": "#000000"},
    "Red":    {"code": "0;31", "fg": "#cc3333"},
    "Green":  {"code": "0;32", "fg": "#33cc33"},
    "Yellow": {"code": "0;33", "fg": "#cccc33"},
    "Blue":   {"code": "0;34", "fg": "#3366cc"},
    "Purple": {"code": "0;35", "fg": "#9933cc"},
    "Cyan":   {"code": "0;36", "fg": "#33cccc"},
    "White":  {"code": "0;37", "fg": "#eeeeee"},

    // Bold
    "Bold Black":  {"code": "1;30", "fg": "#555555"},
    "Bold Red":    {"code": "1;31", "fg": "#ff5555"},
    "Bold Green":  {"code": "1;32", "fg": "#55ff55"},
    "Bold Yellow": {"code": "1;33", "fg": "#ffff55"},
    "Bold Blue":   {"code": "1;34", "fg": "#5599ff"},
    "Bold Purple": {"code": "1;35", "fg": "#cc66ff"},
    "Bold Cyan":   {"code": "1;36", "fg": "#55ffff"},
    "Bold White":  {"code": "1;37", "fg": "#ffffff"},

    // Bright
    "Bright Black":  {"code": "0;90", "fg": "#777777"},
    "Bright Red":    {"code": "0;91", "fg": "#ff4444"},
    "Bright Green":  {"code": "0;92", "fg": "#44ff44"},
    "Bright Yellow": {"code": "0;93", "fg": "#ffff44"},
    "Bright Blue":   {"code": "0;94", "fg": "#4488ff"},
    "Bright Purple": {"code": "0;95", "fg": "#ff44ff"},
    "Bright Cyan":   {"code": "0;96", "fg": "#44ffff"},
    "Bright White":  {"code": "0;97", "fg": "#ffffff"},

    // Bold Bright
    "Bold Bright Black":  {"code": "1;90", "fg": "#999999"},
    "Bold Bright Red":    {"code": "1;91", "fg": "#ff6666"},
    "Bold Bright Green":  {"code": "1;92", "fg": "#66ff66"},
    "Bold Bright Yellow": {"code": "1;93", "fg": "#ffff66"},
    "Bold Bright Blue":   {"code": "1;94", "fg": "#66aaff"},
    "Bold Bright Purple": {"code": "1;95", "fg": "#ff66ff"},
    "Bold Bright Cyan":   {"code": "1;96", "fg": "#66ffff"},
    "Bold Bright White":  {"code": "1;97", "fg": "#ffffff"},
}

const state = {
  user: "Bold Green",
  sep_text: "@",
  sep_color: "Bold Green",
  host: "Bold Green",
  path: "Bold Blue",
  git: "Bright Red",
  symbol_text: "$",
  symbol_color: "White",
};

function fillSelect(id) {
  const sel = document.getElementById(id);
  Object.keys(ANSI_STYLES).forEach(k => {
    const o = document.createElement("option");
    o.value = k;
    o.textContent = k;
    sel.appendChild(o);
  });
  sel.value = state[id];
}

["user", "sep_color", "host", "path", "git", "symbol_color"].forEach(fillSelect);

function updateState() {
  Object.keys(state).forEach(k => {
    const el = document.getElementById(k);
    if (el) state[k] = el.value;
  });
  render();
}

function span(text, styleName) {
  const s = ANSI_STYLES[styleName];
  const e = document.createElement("span");
  e.textContent = text;
  e.style.color = s.fg;
  e.style.fontWeight = s.code.startsWith("1;") ? "bold" : "normal";
  return e;
}

function render() {
  const p = document.getElementById("preview");
  p.innerHTML = "";
  p.append(
    span("zyrotot", state.user),
    span(state.sep_text, state.sep_color),
    span("debian ", state.host),
    span("~/project ", state.path),
    span("(my_branch) ", state.git),
    span(state.symbol_text, state.symbol_color)
  );

const bashCode = `function color_my_prompt() {
  local __user="\\[\\033[${ANSI_STYLES[state.user].code}m\\]\\u"
  local __sep="\\[\\033[${ANSI_STYLES[state.sep_color].code}m\\]${state.sep_text}"
  local __host="\\[\\033[${ANSI_STYLES[state.host].code}m\\]\\h"
  local __cur_location="\\[\\033[${ANSI_STYLES[state.path].code}m\\]\\w"
  local __git_branch_color="\\[\\033[${ANSI_STYLES[state.git].code}m\\]"
  local __git_branch='$(git branch 2>/dev/null | sed -n "s/^* \\(.*\\)$/ (\\1)/p")'
  local __prompt_tail="\\[\\033[${ANSI_STYLES[state.symbol_color].code}m\\]${state.symbol_text}"
  local __reset="\\[\\033[0m\\]"

  export PS1="$__user$__sep$__host $__cur_location$__git_branch_color$__git_branch $__prompt_tail$__reset "
}
color_my_prompt`.trim();

  document.getElementById("output").textContent = bashCode;
}

document.querySelectorAll("select, input").forEach(el =>
  el.addEventListener("input", updateState)
);

document.getElementById("copy").onclick = () =>
  navigator.clipboard.writeText(
    document.getElementById("output").textContent
  );

render();