use proconio::{input, source::auto::AutoSource};
pub type Score = u64;

pub struct Input {}

impl Input {
    pub fn parse_input(input_str: &str) -> Result<Self, String> {
        let source = AutoSource::from(input_str);
        input! {
            from source,
        }

        Ok(Self {})
    }
}

pub struct Output {}

impl Output {
    pub fn parse_output(output_str: &str) -> Result<Self, String> {
        let source = AutoSource::from(output_str);
        input! {
            from source,
        }
        Ok(Self {})
    }

    pub fn get_max_turn(&self, input: &Input) -> usize {
        0
    }

    pub fn get_state_at_turn(&self, input: &Input, turn: usize) -> () {}

    pub fn calc_score(&self, input: &Input, turn: usize) -> Result<Score, String> {
        Ok(0)
    }
}
