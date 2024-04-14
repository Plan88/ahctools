use itertools::Itertools;
use proconio::{input, marker::Bytes, source::auto::AutoSource};
pub type Score = u64;

pub struct Input {
    pub t: usize,
    pub n: usize,
    pub v: Vec<Vec<u8>>,
    pub h: Vec<Vec<u8>>,
    pub a: Vec<Vec<u64>>,
}

impl Input {
    pub fn parse_input(input_str: &str) -> Result<Self, String> {
        let source = AutoSource::from(input_str);
        input! {
        from source,
        (t, n): (usize, usize),
        mut v: [Bytes; n],
        mut h: [Bytes; n-1],
        a: [[u64; n]; n],
        }

        for i in 0..n {
            for j in 0..n - 1 {
                v[i][j] -= b'0';
            }
        }
        for i in 0..n - 1 {
            for j in 0..n {
                h[i][j] -= b'0';
            }
        }

        Ok(Self { t, n, v, h, a })
    }
}

type Action = (u8, char, char);
pub struct Output {
    pub pi: usize,
    pub pj: usize,
    pub qi: usize,
    pub qj: usize,
    pub actions: Vec<Action>,
}

impl Output {
    pub fn parse_output(output_str: &str) -> Result<Self, String> {
        let lines = output_str.split("\n").collect_vec();

        let init_source = AutoSource::from(lines[0]);
        input! {
        from init_source,
        (pi, pj, qi, qj): (usize, usize, usize, usize),
            }

        let mut actions = vec![];
        for line in lines.into_iter().skip(1) {
            if line == "" {
                continue;
            }
            let source = AutoSource::from(line);
            input! {
            from source,
                    (s, d, e): (u8, char, char),
                }
            actions.push((s, d, e));
        }

        Ok(Self {
            pi,
            pj,
            qi,
            qj,
            actions,
        })
    }

    pub fn get_max_turn(&self, input: &Input) -> usize {
        let mut max_turn = 0;
        let mut x1 = self.pi;
        let mut y1 = self.pj;
        let mut x2 = self.qi;
        let mut y2 = self.qj;

        for &(_, d, e) in self.actions.iter() {
            if let Err(_) = self.is_valid_move(x1, y1, d, input) {
                return max_turn;
            }
            if let Err(_) = self.is_valid_move(x2, y2, e, input) {
                return max_turn;
            }

            (x1, y1) = self.get_next(x1, y1, d);
            (x2, y2) = self.get_next(x2, y2, e);
            max_turn += 1;
        }
        max_turn
    }

    pub fn get_state_at_turn(
        &self,
        input: &Input,
        turn: usize,
    ) -> ((usize, usize), (usize, usize), Vec<Vec<u64>>) {
        let mut x1 = self.pi;
        let mut y1 = self.pj;
        let mut x2 = self.qi;
        let mut y2 = self.qj;
        let mut a = input.a.clone();

        for &(s, d, e) in self.actions.iter().take(turn) {
            if s == 1 {
                let t = a[x1][y1];
                a[x1][y1] = a[x2][y2];
                a[x2][y2] = t;
            }

            (x1, y1) = self.get_next(x1, y1, d);
            (x2, y2) = self.get_next(x2, y2, e);
        }

        ((x1, y1), (x2, y2), a)
    }

    pub fn calc_score(&self, input: &Input, turn: usize) -> Result<Score, String> {
        let mut x1 = self.pi;
        let mut y1 = self.pj;
        let mut x2 = self.qi;
        let mut y2 = self.qj;
        let mut a = input.a.clone();

        for (i, &(s, d, e)) in self.actions.iter().enumerate().take(turn) {
            if s == 1 {
                let t = a[x1][y1];
                a[x1][y1] = a[x2][y2];
                a[x2][y2] = t;
            }
            if let Err(s) = self.is_valid_move(x1, y1, d, input) {
                return Err(s + &format!("at turn {}", i + 1));
            }
            if let Err(s) = self.is_valid_move(x2, y2, e, input) {
                return Err(s + &format!("at turn {}", i + 1));
            }

            (x1, y1) = self.get_next(x1, y1, d);
            (x2, y2) = self.get_next(x2, y2, e);
        }

        let d1 = self.eval_grid(&input.a, input) as f64;
        let d2 = self.eval_grid(&a, input) as f64;
        let rate = d1 / d2;
        let log = rate.log2();
        let score = 0.max((1_000_000.0 * log).floor() as u64);
        Ok(score)
    }

    fn get_next(&self, x: usize, y: usize, d: char) -> (usize, usize) {
        match d {
            'L' => (x, y - 1),
            'R' => (x, y + 1),
            'U' => (x - 1, y),
            'D' => (x + 1, y),
            _ => (x, y),
        }
    }

    fn is_valid_move(&self, x: usize, y: usize, d: char, input: &Input) -> Result<(), String> {
        match d {
            'L' => {
                if y == 0 {
                    return Err(format!(
                        "Cannot move out of grid, attempt to left from {}, {}",
                        x, y,
                    ));
                }
                let v = input.v[x][y - 1];
                if v == 1 {
                    return Err(format!(
                        "Cannot move beyond the wall, attempt to left from {}, {}",
                        x, y,
                    ));
                }
            }
            'R' => {
                if y == input.n - 1 {
                    return Err(format!(
                        "Cannot move out of grid, attempt to right from {}, {}",
                        x, y,
                    ));
                }
                let v = input.v[x][y];
                if v == 1 {
                    return Err(format!(
                        "Cannot move beyond the wall, attempt to right from {}, {}",
                        x, y,
                    ));
                }
            }
            'U' => {
                if x == 0 {
                    return Err(format!(
                        "Cannot move out of grid, attempt to up from {}, {}",
                        x, y,
                    ));
                }
                let h = input.h[x - 1][y];
                if h == 1 {
                    return Err(format!(
                        "Cannot move beyond the wall, attempt to up from {}, {}",
                        x, y,
                    ));
                }
            }
            'D' => {
                if x == input.n - 1 {
                    return Err(format!(
                        "Cannot move out of grid, attempt to down from {}, {}",
                        x, y,
                    ));
                }
                let h = input.h[x][y];
                if h == 1 {
                    return Err(format!(
                        "Cannot move beyond the wall, attempt to down from {}, {}",
                        x, y,
                    ));
                }
            }
            _ => (),
        }

        Ok(())
    }

    fn eval_grid(&self, a: &Vec<Vec<u64>>, input: &Input) -> u64 {
        let n = input.n;
        let mut score = 0;

        for i in 0..n {
            for j in 0..n - 1 {
                let v = input.v[i][j];
                if v == 1 {
                    continue;
                }
                let a1 = a[i][j];
                let a2 = a[i][j + 1];
                score += (a1 - a2) * (a1 - a2);
            }
        }
        for i in 0..n - 1 {
            for j in 0..n {
                let h = input.h[i][j];
                if h == 1 {
                    continue;
                }
                let a1 = a[i][j];
                let a2 = a[i + 1][j];
                score += (a1 - a2) * (a1 - a2);
            }
        }

        score
    }
}
