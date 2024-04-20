use svg::Document;
use wasm_bindgen::prelude::*;
mod element;
// mod generator_a;
// mod io;
mod rnd;
mod tools;

#[wasm_bindgen]
pub fn gen(seed: i32) -> String {
    let input = tools::gen(seed as u64);
    input.to_string()
}

#[wasm_bindgen(getter_with_clone)]
pub struct Ret {
    pub score: i64,
    pub err: String,
    pub svg: String,
}

const SVG_SIZE: usize = 600;
const MAP_SIZE: f64 = 200000.0;
const GETA: f64 = 100000.0;

/// input, output, turnが与えられたときに
/// スコア、エラー文、svgの画像のstringを返す関数
#[wasm_bindgen]
pub fn vis(input: String, output: String, turn: usize) -> Ret {
    let input = tools::parse_input(&input);
    let output = tools::parse_output(&input, &output);
    let (mut score, err);

    match output.clone() {
        Ok(out) => {
            let (s, e) = tools::compute_score(&input, &out);
            score = s;
            err = e;
        }
        Err(e) => {
            score = 0;
            err = e;
        }
    }

    let mut svg = Document::new()
        .set("viewBox", (0, 0, SVG_SIZE, SVG_SIZE))
        .set("width", SVG_SIZE)
        .set("height", SVG_SIZE)
        .to_string();
    if let Ok(out) = output.clone() {
        let (svg2, crt_score) = get_svg_string(input, out, turn);
        svg = svg2;

        if turn > 0 {
            score = crt_score;
        }
    }
    Ret {
        score,
        err,
        svg: svg.to_string(),
    }
}

fn get_svg_string(input: tools::Input, output: tools::Output, turn: usize) -> (String, i64) {
    let sim = simulate(&input, &output, turn);

    let mut svg = Document::new()
        .set("viewBox", (0, 0, SVG_SIZE, SVG_SIZE))
        .set("width", SVG_SIZE)
        .set("height", SVG_SIZE);

    // wall
    for &(lx, ly, rx, ry) in input.walls.iter() {
        let lx = f(lx);
        let ly = f(ly);
        let rx = f(rx);
        let ry = f(ry);

        svg = svg.add(element::line(lx, ly, rx, ry, "black"))
    }

    // distination
    for (i, &(x, y)) in input.ps.iter().enumerate() {
        let color = if sim.visited[i] { "red" } else { "blud" };
        let x = f(x);
        let y = f(y);

        svg = svg.add(element::circle(x, y, 3, color))
    }

    // current position
    let (cx, cy) = (g(sim.p.0), g(sim.p.1));
    svg = svg.add(element::circle(cx, cy, 3, "black"));

    (svg.to_string(), sim.crt_score)
}

fn f(x: i64) -> usize {
    let x = x as f64 + GETA;
    let r = x / MAP_SIZE;

    (SVG_SIZE as f64 * r).round() as usize
}
fn g(x: f64) -> usize {
    let x = x + GETA;
    let r = x / MAP_SIZE;

    (SVG_SIZE as f64 * r).round() as usize
}

fn simulate(input: &tools::Input, output: &tools::Output, turn: usize) -> tools::Sim {
    let mut sim = tools::Sim::new(input);

    for &(mv, ax, ay) in output.out.iter().take(turn) {
        let (c, q, d) = sim.query(input, mv, ax, ay);
    }

    sim
}

#[wasm_bindgen]
pub fn get_max_turn(_input: String, output: String) -> usize {
    let mut turn = 0;
    for line in output.split('\n') {
        if line.starts_with("#") {
            continue;
        }
        turn += 1;
    }
    turn
}
