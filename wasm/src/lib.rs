use svg::Document;
use wasm_bindgen::prelude::*;
mod element;
mod generator;
mod io;
mod rnd;

#[wasm_bindgen]
pub fn gen(seed: i32) -> String {}

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

    svg.to_string()
}

#[wasm_bindgen]
pub fn get_max_turn(input: String, output: String) -> usize {
    io::Output::parse_output(&output)
        .unwrap()
        .get_max_turn(&io::Input::parse_input(&input).unwrap())
}
