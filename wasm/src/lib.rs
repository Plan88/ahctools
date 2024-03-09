use svg::Document;
use wasm_bindgen::prelude::*;
mod element;
mod generator;
mod io;
mod rnd;

#[wasm_bindgen]
pub fn gen(seed: i32) -> String {
    let mut s = generator::IN_FIXED[seed as usize % 20].to_string();
    s += &rnd::gen_permutation(seed as u64);

    s
}

#[wasm_bindgen(getter_with_clone)]
pub struct Ret {
    pub score: io::Score,
    pub err: String,
    pub svg: String,
}

/// input, output, turnが与えられたときに
/// スコア、エラー文、svgの画像のstringを返す関数
#[wasm_bindgen]
pub fn vis(input: String, output: String, turn: usize) -> Ret {
    let input = io::Input::parse_input(&input).unwrap();
    let output = io::Output::parse_output(&output).unwrap();

    let mut score = 0;
    let mut err = "".to_string();

    match output.calc_score(&input, turn) {
        Ok(s) => score = s,
        Err(s) => err = s,
    }

    Ret {
        score,
        err,
        svg: get_svg_string(input, output, turn),
    }
}

const SVG_SIZE: usize = 600;

fn get_svg_string(input: io::Input, output: io::Output, turn: usize) -> String {
    let mut svg = Document::new()
        .set("viewBox", (0, 0, SVG_SIZE, SVG_SIZE))
        .set("width", SVG_SIZE)
        .set("height", SVG_SIZE);

    let n = input.n;
    let d = SVG_SIZE / n;

    let ((pi, pj), (qi, qj), a) = output.get_state_at_turn(&input, turn);

    svg = svg.add(element::line(0, 0, 0, SVG_SIZE, "black"));
    svg = svg.add(element::line(0, SVG_SIZE, SVG_SIZE, SVG_SIZE, "black"));
    svg = svg.add(element::line(SVG_SIZE, SVG_SIZE, SVG_SIZE, 0, "black"));
    svg = svg.add(element::line(SVG_SIZE, 0, 0, 0, "black"));

    let n2 = n as f64 * n as f64;
    for i in 0..n {
        for j in 0..n {
            let aij = a[i][j] as f64;
            let scale = aij / n2;
            svg = svg.add(element::rectangle(
                j * d,
                i * d,
                d,
                d,
                &element::color(scale),
            ));
        }
    }

    for i in 0..n {
        for j in 0..n - 1 {
            let vij = input.v[i][j];
            if vij == 1u8 {
                let x1 = j * d + d;
                let y1 = i * d;
                let x2 = x1;
                let y2 = y1 + d;
                svg = svg.add(element::line(x1, y1, x2, y2, "black"));
            }
        }
    }

    for i in 0..n - 1 {
        for j in 0..n {
            let hij = input.h[i][j];
            if hij == 1u8 {
                let x1 = j * d;
                let y1 = i * d + d;
                let x2 = x1 + d;
                let y2 = y1;
                svg = svg.add(element::line(x1, y1, x2, y2, "black"));
            }
        }
    }

    svg = svg.add(element::circle(
        pj * d + d / 2,
        pi * d + d / 2,
        d / 3,
        "red",
    ));
    svg = svg.add(element::circle(
        qj * d + d / 2,
        qi * d + d / 2,
        d / 3,
        "blue",
    ));

    svg.to_string()
}

#[wasm_bindgen]
pub fn get_max_turn(input: String, output: String) -> usize {
    io::Output::parse_output(&output)
        .unwrap()
        .get_max_turn(&io::Input::parse_input(&input).unwrap())
}
