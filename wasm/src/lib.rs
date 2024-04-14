use itertools::Itertools;
use svg::Document;
use wasm_bindgen::prelude::*;
mod element;
mod generator;
mod io;
mod rnd;

#[wasm_bindgen]
pub fn gen(seed: i32) -> String {
    let mut rng = rnd::RNG::new(seed as u64);
    let n = rng.gen_range(9, 9, true);
    let m = rng.gen_range(20, 20, true);
    let k = rng.gen_range(81, 81, true);
    let mut a = vec![vec![0; n]; n];
    let mut s = vec![vec![vec![0; 3]; 3]; m];

    for i in 0..n {
        for j in 0..n {
            a[i][j] = rng.gen_range(0, 998244353, false);
        }
    }
    for i in 0..m {
        for j in 0..3 {
            for k in 0..3 {
                s[i][j][k] = rng.gen_range(0, 998244353, false);
            }
        }
    }

    let mut input = format!("{} {} {}", n, m, k) + "\n";

    for i in 0..n {
        input += &a[i].iter().join(" ");
        input += &"\n"
    }
    for i in 0..m {
        for j in 0..3 {
            input += &s[i][j].iter().join(" ");
            input += &"\n";
        }
    }

    input
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

const SVG_SIZE: usize = 603;

fn get_svg_string(input: io::Input, output: io::Output, turn: usize) -> String {
    let mut svg = Document::new()
        .set("viewBox", (0, 0, SVG_SIZE, SVG_SIZE))
        .set("width", SVG_SIZE)
        .set("height", SVG_SIZE);

    let n = input.n;
    let d = SVG_SIZE / n;
    let a = output.get_state_at_turn(&input, turn);

    for i in 0..n {
        for j in 0..n {
            svg = svg.add(element::rectangle(
                j * d,
                i * d,
                d,
                d,
                &element::color(a[i][j] as f64 / 998244353f64),
            ));
        }
    }

    for i in 0..n + 1 {
        let x1 = 0;
        let x2 = SVG_SIZE;
        let y1 = i * d;
        let y2 = y1;
        let color = "black";
        svg = svg.add(element::line(x1, y1, x2, y2, color))
    }
    for i in 0..n + 1 {
        let y1 = 0;
        let y2 = SVG_SIZE;
        let x1 = i * d;
        let x2 = x1;
        let color = "black";
        svg = svg.add(element::line(x1, y1, x2, y2, color))
    }
    for i in 0..n {
        for j in 0..n {
            svg = svg.add(element::text(
                j * d + d / 2,
                i * d + d / 2,
                &a[i][j].to_string(),
                10,
            ));
        }
    }

    svg.to_string()
}

#[wasm_bindgen]
pub fn get_max_turn(input: String, output: String) -> usize {
    io::Output::parse_output(&output)
        .unwrap()
        .get_max_turn(&io::Input::parse_input(&input).unwrap())
}
