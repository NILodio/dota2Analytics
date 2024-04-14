export type Body_login_login_access_token = {
  grant_type?: string | null;
  username: string;
  password: string;
  scope?: string;
  client_id?: string | null;
  client_secret?: string | null;
};

export type HTTPValidationError = {
  detail?: Array<ValidationError>;
};

export type ItemCreate = {
  title: string;
  description?: string | null;
};

export type HeroPollCreate = {
  hero_id: number;
  hero_name: string;
  team: string;
  description?: string | null;
};

export type ItemOut = {
  title: string;
  description?: string | null;
  id: number;
  owner_id: number;
};

export type ItemUpdate = {
  title?: string | null;
  description?: string | null;
};

export type ItemsOut = {
  data: Array<ItemOut>;
  count: number;
};

export type Message = {
  message: string;
};

export type NewPassword = {
  token: string;
  new_password: string;
};

export type Token = {
  access_token: string;
  token_type?: string;
};

export type UpdatePassword = {
  current_password: string;
  new_password: string;
};

export type UserCreate = {
  email: string;
  is_active?: boolean;
  is_superuser?: boolean;
  full_name?: string | null;
  password: string;
};

export type UserOut = {
  email: string;
  is_active?: boolean;
  is_superuser?: boolean;
  full_name?: string | null;
  id: number;
};

export type UserRegister = {
  email: string;
  password: string;
  full_name?: string | null;
};

export type UserUpdate = {
  email?: string | null;
  is_active?: boolean;
  is_superuser?: boolean;
  full_name?: string | null;
  password?: string | null;
};

export type UserUpdateMe = {
  full_name?: string | null;
  email?: string | null;
};

export type UsersOut = {
  data: Array<UserOut>;
  count: number;
};

export type ValidationError = {
  loc: Array<string | number>;
  msg: string;
  type: string;
};

export interface Hero {
  id: number;
  localized_name: string;
  primary_attr: "str" | "agi" | "int" | "all";
  attack_type: string;
  roles: Array<string>;
}

export type HeroAttr = "str" | "agi" | "int" | "all";

export type SetHeroAttr = (value: HeroAttr) => void;
export type SetHeroFilter = (value: string) => void;

export type HeroOut = {
  id: number;
  name: string;
  localized_name: string;
  primary_attr: "str" | "agi" | "int" | "all";
  attack_type: string;
  roles: Array<string>;
};

export type HeroesOut = {
  data: Array<HeroOut>;
  count: number;
};

export type PollCreate = {
  hero_id: number;
  hero_name: string;
  team: string;
  player_name?: string | null;
  description?: string | null;
};

export type PollOut = {
  id: number;
  hero_id: number;
  team_id: number;
  hero_name: string;
  team: string;
  player_name?: string | null;
  description?: string | null;
};

export type PollUpdate = {
  hero_id?: number | null;
  hero_name?: string | null;
  team?: string | null;
  player_name?: string | null;
  description?: string | null;
};

export type PollsOut = {
  data: Array<PollOut>;
  count: number;
};

export type PredictOut = {
  prediction: number;
  message: string;
};
